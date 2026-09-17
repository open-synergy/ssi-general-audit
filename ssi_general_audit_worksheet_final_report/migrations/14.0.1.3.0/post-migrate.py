# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.2.0 -> 14.0.1.3.0
#
# Changes: general_audit_ws_b66777d.lai_number used to be filled by
#          `default=` on create (GitHub issue #360, first revision). It is
#          now filled by the `_10_generate_lai_number` post_open_action
#          hook instead, so it only gets a value the first time a
#          worksheet is opened (`action_open`). Records that were already
#          past `draft` before this change was installed already ran
#          `action_open` in the past -- under the OLD code, so the hook
#          that assigns `lai_number` never ran for them -- and will never
#          run `action_open` again, since that is a one-way transition
#          (odoo-development skill, 10-migration-script.md Kelompok A:
#          "mekanisme pemilihan berpindah" from `default=` to a state-change
#          hook). Without this backfill those records would carry an empty
#          `lai_number` forever. Uses the ORM (not raw SQL) because the
#          backfill needs to call the `ir.sequence` model method
#          `next_by_code`, which has no SQL equivalent (openupgradelib
#          10-migration-script.md: "Pakai ORM hanya bila logikanya memang
#          butuh (mis. memanggil method model)"). Runs `post-migrate`,
#          not `pre-migrate`, because it reads/writes through the ORM
#          (`env["general_audit_ws_b66777d"].search(...)`), which requires
#          the model to already be loaded in the registry.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Backfill ``lai_number`` for worksheets already past ``draft``.

    Targets every ``general_audit_ws_b66777d`` record whose ``state`` is
    no longer ``draft`` and whose ``lai_number`` is still empty -- these
    already ran ``action_open`` under the old code, before the
    ``_10_generate_lai_number`` hook existed, and will never run
    ``action_open`` again. Processed in ascending ``id`` order (creation
    order) so the assigned numbers stay in the same order the records
    were created, one ``ir.sequence.next_by_code`` call per record.
    Idempotent: a record already carrying a ``lai_number`` is excluded
    by the search domain, so re-running this script on an already
    migrated database assigns nothing new.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; writes ``lai_number`` on the targeted records
    """
    Worksheet = env["general_audit_ws_b66777d"]
    records = Worksheet.search(
        [
            ("state", "!=", "draft"),
            "|",
            ("lai_number", "=", False),
            ("lai_number", "=", ""),
        ],
        order="id asc",
    )
    Sequence = env["ir.sequence"]
    for record in records:
        record.lai_number = Sequence.next_by_code("general_audit_ws_b66777d.lai_number")
    _logger.info(
        "Backfilled lai_number on %s general_audit_ws_b66777d record(s).",
        len(records),
    )
