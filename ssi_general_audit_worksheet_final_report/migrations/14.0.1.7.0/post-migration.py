# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.6.0 -> 14.0.1.7.0
#
# Changes: the Final Team Allocations figures of
#          general_audit_ws_b66777d change from Integer minutes to
#          Float hours. This script divides the four per-row columns
#          of general_audit_ws_b66777d_team_allocation by 60 and
#          rebuilds the stored total_* and diff_* fields of every
#          general_audit_ws_b66777d worksheet. The awp_total_* columns
#          are left as they are: their source is already in hours, and
#          they are refreshed by the next Populate click.
#
# This is a "post" script: the column types are already float when it
# runs, so the division keeps its decimals.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_ROW_COLUMNS = (
    "pe_allocation",
    "ra_allocation",
    "rr_allocation",
    "reporting_allocation",
)

_TOTAL_FIELDS = (
    "total_pe_allocation",
    "total_ra_allocation",
    "total_rr_allocation",
    "total_reporting_allocation",
    "total_allocation",
)

_DIFF_FIELDS = (
    "diff_pe_allocation",
    "diff_ra_allocation",
    "diff_rr_allocation",
    "diff_reporting_allocation",
    "diff_allocation",
)


@openupgrade.migrate()
def migrate(env, version):
    """Convert stored allocation minutes to hours.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates the team allocation rows and rebuilds the
        stored totals and differences of the worksheets
    """
    assignments = ", ".join(
        "%s = %s / 60.0" % (column, column) for column in _ROW_COLUMNS
    )
    rows = openupgrade.logged_query(
        env.cr,
        "UPDATE general_audit_ws_b66777d_team_allocation SET " + assignments,
    )
    _logger.info("Converted %s team allocation row(s) to hours.", rows)

    worksheets = env["general_audit_ws_b66777d"].search([])
    for field_name in _TOTAL_FIELDS + _DIFF_FIELDS:
        env.add_to_compute(worksheets._fields[field_name], worksheets)
    worksheets.flush(list(_TOTAL_FIELDS + _DIFF_FIELDS))
    _logger.info("Recomputed allocation totals on %s worksheet(s).", len(worksheets))
