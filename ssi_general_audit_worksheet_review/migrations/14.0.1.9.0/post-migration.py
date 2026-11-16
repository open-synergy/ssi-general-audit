# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.8.0 -> 14.0.1.9.0
#
# Changes: Proposed Audit Opinion is no longer a conclusion source of the
#          Audit Final Memorandum. Dropping an ``(4, ref)`` command from the
#          data file does not remove the many2many link already stored in an
#          existing database, and the conclusion lines created earlier can
#          not be deleted from the user interface, so both are cleaned here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_MEMO_TYPE_XML_ID = "ssi_general_audit_worksheet_final_report.worksheet_type_a8c54f3"
_REMOVED_TYPE_XML_ID = "ssi_general_audit_worksheet_review.worksheet_type_fc75636"


@openupgrade.migrate()
def migrate(env, version):
    """Unlink Proposed Audit Opinion and delete its conclusion lines.

    A line that holds a summary typed by the user (several worksheets of
    the type exist and the text is filled) is kept and reported in the log,
    so no typed text is lost silently. Every other line only mirrors a
    worksheet conclusion and is deleted.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates the memorandum worksheet type and deletes
        ``general_audit_ws_a8c54f3.conclusion`` rows
    """
    memo_type = env.ref(_MEMO_TYPE_XML_ID, raise_if_not_found=False)
    removed = env.ref(_REMOVED_TYPE_XML_ID, raise_if_not_found=False)
    if not memo_type or not removed:
        return
    memo_type.write({"conclusion_source_type_ids": [(3, removed.id)]})
    lines = env["general_audit_ws_a8c54f3.conclusion"].search(
        [("type_id", "=", removed.id)]
    )
    kept = lines.filtered(lambda line: line.worksheet_count > 1 and line.conclusion)
    to_delete = lines - kept
    _logger.info(
        "Deleting %s conclusion line(s) of Proposed Audit Opinion.",
        len(to_delete),
    )
    to_delete.unlink()
    if kept:
        _logger.warning(
            "Kept %s conclusion line(s) holding a typed summary: ids %s.",
            len(kept),
            kept.ids,
        )
