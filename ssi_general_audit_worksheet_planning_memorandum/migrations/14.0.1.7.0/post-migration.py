# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.6.0 -> 14.0.1.7.0
#
# Changes: 8 Link fields of general_audit_ws_fbbe0f8 are now Many2many
#          link_N_ids. A newly created many2many relation table is not
#          filled by Odoo, so existing worksheets would show empty
#          links until their next Reload. assignment_team_ids is stored
#          and computed from link_9_ids, so it is rebuilt as well. This
#          script rebuilds these fields on every worksheet.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_LINK_NUMBERS = (9, 15, 16, 17, 18, 23, 25, 26)


@openupgrade.migrate()
def migrate(env, version):
    """Rebuild the stored Many2many Link fields of every worksheet.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes ``link_N_ids`` and ``assignment_team_ids``
    """
    worksheets = env["general_audit_ws_fbbe0f8"].search([])
    names = ["link_%d_ids" % number for number in _LINK_NUMBERS]
    names.append("assignment_team_ids")
    for name in names:
        env.add_to_compute(worksheets._fields[name], worksheets)
    worksheets.flush(names)
    _logger.info(
        "Recomputed %s field(s) on %s worksheet(s).",
        len(names),
        len(worksheets),
    )
