# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.7.0 -> 14.0.1.8.0
#
# Changes: 21 Link fields of general_audit_ws_a8c54f3 are now Many2many
#          link_N_ids. A newly created many2many relation table is not
#          filled by Odoo, so existing worksheets would show empty
#          links until their next Reload. This script rebuilds every
#          link_N_ids of every worksheet.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_LINK_NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
_LINK_NUMBERS += (22, 23, 25, 27)


@openupgrade.migrate()
def migrate(env, version):
    """Rebuild the stored Many2many Link fields of every worksheet.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes the ``link_N_ids`` fields
    """
    worksheets = env["general_audit_ws_a8c54f3"].search([])
    names = ["link_%d_ids" % number for number in _LINK_NUMBERS]
    for name in names:
        env.add_to_compute(worksheets._fields[name], worksheets)
    worksheets.flush(names)
    _logger.info(
        "Recomputed %s Link field(s) on %s worksheet(s).",
        len(names),
        len(worksheets),
    )
