# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.4.1 -> 14.0.1.4.2
#
# Changes: Total Equity and Total Liability and Equity gained the
#          Comprehensive Income components and T006, the adjustment columns
#          of the Total lines with subtracted components are now zero, and
#          the display order comes from the new layout master data. The
#          amounts of existing Total posture lines are stored computes and
#          are not refreshed by a module update, and their order is only
#          applied on Reload, so both are refreshed here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_AMOUNT_FIELDS = (
    "unaudited",
    "adjustment_debit",
    "adjustment_credit",
    "adjustment_visible",
    "audited",
    "previous",
)


@openupgrade.migrate()
def migrate(env, version):
    """Refresh the amounts and the order of existing posture lines.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``general_audit_ws_ff42fdc.posture`` rows
    """
    Posture = env["general_audit_ws_ff42fdc.posture"]
    lines = Posture.search([("line_type", "=", "total")])
    for field_name in _AMOUNT_FIELDS:
        env.add_to_compute(Posture._fields[field_name], lines)
    lines.flush(list(_AMOUNT_FIELDS))
    _logger.info("Recomputed amounts on %s total posture line(s).", len(lines))

    worksheets = env["general_audit_ws_ff42fdc"].search([])
    for worksheet in worksheets.filtered("posture_ids"):
        worksheet._resequence_posture_lines()
    _logger.info("Resequenced posture lines of %s worksheet(s).", len(worksheets))
