# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
#
# Migration: 14.0.1.2.3 -> 14.0.1.2.4
#
# Changes: general_audit_ws_bcc0d76._populate(), before commit 7ca3db3,
#          searched general_audit_worksheet without filtering on
#          general_audit_id, so detail lines created before that fix can
#          point (general_worksheet_id) at a worksheet belonging to a
#          DIFFERENT engagement than their own worksheet_id's audit.
#          Commit 7ca3db3 scoped the search correctly for new lines, and
#          f664e7e added a guard in _populate() that refuses to unlink a
#          detail line still referenced by a
#          general_audit_ws_cae598e_detail.detail_id (to avoid a
#          ForeignKeyViolation on that ondelete="restrict" relation).
#          Together those two fixes mean a stale line that was already
#          evaluated in cae598e can never be cleaned up by _populate()
#          itself, no matter how many times it runs afterwards (GitHub
#          issue #373). This script fixes the data already on disk:
#
#          Step 1 calls _populate() (ORM) on every
#          general_audit_ws_bcc0d76 record so any correct
#          (worksheet_id, parent_type_id) pair missing a detail line
#          gets one -- this is the same method action_populate() calls,
#          now safe to call directly since 7ca3db3 already scopes it to
#          general_audit_id.
#
#          Step 2 finds the stale lines with a SQL join (not ORM, so it
#          reads as one set instead of triggering per-row computes).
#
#          Step 3 repoints general_audit_ws_cae598e_detail.detail_id from
#          each stale line to its correct counterpart -- found by
#          matching worksheet_id + parent_type_id, filtered to the pair
#          whose general_worksheet_id truly belongs to the parent's
#          audit -- then deletes the stale line. The repoint MUST run
#          before the DELETE: general_audit_ws_cae598e_detail.detail_id
#          is ondelete="restrict" (models/ga_cae598e/
#          general_audit_ws_cae598e_detail.py:38-40), so deleting a
#          still-referenced stale row raises
#          psycopg2.errors.ForeignKeyViolation and rolls back the whole
#          migration.
#
#          Step 4: a stale line with no correct counterpart (its
#          worksheet type no longer qualifies as main_worksheet, or some
#          other unforeseen case) is left untouched and logged as a
#          warning for manual review -- deleting or repointing it would
#          be guessing.
#
#          This script is safe to run more than once: after one clean
#          run, step 1 is a no-op (every qualifying pair already has a
#          line) and step 2's SELECT returns no rows.
#
#          Step 1 needs an explicit flush() before step 2/3's raw SQL.
#          Detail.create() inserts a new row right away, but
#          parent_type_id/code_internal/sequence are related(store=True)
#          fields Odoo defers computing until the next ORM read/write or
#          an explicit flush -- cr.execute() is raw SQL and never
#          triggers that on its own. Without the flush, a detail line
#          step 1 just created for the correct worksheet still has
#          parent_type_id = NULL in the database when step 3's SELECT
#          runs, so it is never matched as the "correct counterpart" of
#          the stale line it was meant to replace, and the stale line is
#          wrongly logged as having none. Caught locally while testing
#          this migration against a database with real stale data
#          (issue #373, 237 stale lines total): before the flush was
#          added, only the 37 stale lines whose correct counterpart
#          already existed BEFORE this script ran got repointed; the
#          other 200 were wrongly logged as "no correct counterpart",
#          including 166 whose counterpart step 1 had in fact just
#          created moments earlier in the very same run. Adding the
#          flush let a second run repoint those 166 as well, leaving
#          only the 34 lines that genuinely have no counterpart (their
#          audit never had its own worksheet of that type at all).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Repoint evaluated cae598e references off stale bcc0d76 lines.

    Calls ``general_audit_ws_bcc0d76._populate()`` on every record to
    backfill any correct ``(worksheet_id, parent_type_id)`` detail line
    that is still missing, then finds ``general_audit_ws_bcc0d76.detail``
    rows whose ``general_worksheet_id`` belongs to a different
    ``general_audit_id`` than their own worksheet's audit (stale rows
    created by the pre-7ca3db3 ``_populate()`` bug). For each stale row
    with a correct counterpart, repoints any
    ``general_audit_ws_cae598e_detail.detail_id`` pointing at it onto
    the correct row, then deletes the stale row. Stale rows without a
    correct counterpart are left in place and logged as a warning.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``general_audit_ws_cae598e_detail`` rows
        and deletes stale ``general_audit_ws_bcc0d76_detail`` rows
    """
    cr = env.cr

    # Step 1: backfill missing correct (worksheet_id, parent_type_id)
    # pairs via the model's own, already-fixed populate logic.
    worksheets = env["general_audit_ws_bcc0d76"].search([])
    for worksheet in worksheets:
        worksheet._populate()
    _logger.info(
        "Ran _populate() on %s general_audit_ws_bcc0d76 record(s).",
        len(worksheets),
    )

    # Flush the stored related fields (parent_type_id, code_internal,
    # sequence) that _populate()'s Detail.create() calls just triggered
    # a compute for. Odoo defers writing those to the database until
    # the next ORM read/write or an explicit flush; the raw cr.execute()
    # calls below never trigger that on their own, so without this a
    # line step 1 just created is invisible to step 3's matching query.
    env["general_audit_ws_bcc0d76.detail"].flush()

    # Step 2: identify stale detail lines -- their general_worksheet_id
    # points to a worksheet whose general_audit_id differs from the
    # audit of their own parent worksheet_id (or points nowhere).
    cr.execute(
        """
        SELECT d.id, d.worksheet_id, d.parent_type_id
        FROM general_audit_ws_bcc0d76_detail d
        JOIN general_audit_ws_bcc0d76 b ON b.id = d.worksheet_id
        JOIN general_audit_worksheet gw_parent
            ON gw_parent.id = b.worksheet_id
        LEFT JOIN general_audit_worksheet gw_ref
            ON gw_ref.id = d.general_worksheet_id
        WHERE gw_ref.general_audit_id IS DISTINCT FROM gw_parent.general_audit_id
        """
    )
    stale_rows = cr.fetchall()

    repointed = 0
    deleted = 0
    no_match = 0
    for stale_id, bcc0d76_id, parent_type_id in stale_rows:
        # Step 3: look for the correct counterpart -- same worksheet_id
        # and parent_type_id, whose general_worksheet_id really belongs
        # to the parent worksheet's own audit (i.e. is NOT stale).
        cr.execute(
            """
            SELECT d.id
            FROM general_audit_ws_bcc0d76_detail d
            JOIN general_audit_ws_bcc0d76 b ON b.id = d.worksheet_id
            JOIN general_audit_worksheet gw_parent
                ON gw_parent.id = b.worksheet_id
            JOIN general_audit_worksheet gw_ref
                ON gw_ref.id = d.general_worksheet_id
            WHERE d.worksheet_id = %s
              AND d.parent_type_id IS NOT DISTINCT FROM %s
              AND d.id != %s
              AND gw_ref.general_audit_id = gw_parent.general_audit_id
            """,
            (bcc0d76_id, parent_type_id, stale_id),
        )
        match = cr.fetchone()
        if match is None:
            no_match += 1
            _logger.warning(
                "No correct counterpart for stale "
                "general_audit_ws_bcc0d76_detail id=%s "
                "(worksheet_id=%s, parent_type_id=%s) -- left "
                "untouched for manual review.",
                stale_id,
                bcc0d76_id,
                parent_type_id,
            )
            continue

        correct_id = match[0]

        # Repoint FIRST: general_audit_ws_cae598e_detail.detail_id is
        # ondelete="restrict" onto this table, so deleting the stale
        # row before repointing raises a ForeignKeyViolation.
        rows = openupgrade.logged_query(
            cr,
            """
            UPDATE general_audit_ws_cae598e_detail
            SET detail_id = %s
            WHERE detail_id = %s
            """,
            (correct_id, stale_id),
        )
        repointed += rows

        openupgrade.logged_query(
            cr,
            "DELETE FROM general_audit_ws_bcc0d76_detail WHERE id = %s",
            (stale_id,),
        )
        deleted += 1

    _logger.info(
        "Stale bcc0d76.detail cleanup: %s stale row(s) found, %s "
        "cae598e_detail reference(s) repointed, %s stale row(s) "
        "deleted, %s left untouched without a correct counterpart.",
        len(stale_rows),
        repointed,
        deleted,
        no_match,
    )
