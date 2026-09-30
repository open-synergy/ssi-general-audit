# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.7.0 -> 14.0.1.8.0
#
# Changes: 21 Link fields of general_audit_ws_a8c54f3 change from
#          Many2one link_N_id to Many2many link_N_ids, because their
#          worksheet types allow more than one worksheet per audit.
#          Odoo leaves the column of a removed field in place, so this
#          script drops the old link_N_id columns. The new link_N_ids
#          values are rebuilt by the post-migration script.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_TABLE = "general_audit_ws_a8c54f3"

_LINK_NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
_LINK_NUMBERS += (22, 23, 25, 27)


@openupgrade.migrate()
def migrate(env, version):
    """Drop the Many2one columns replaced by Many2many Link fields.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; drops the old ``link_N_id`` columns
    """
    columns = [
        (_TABLE, "link_%d_id" % number)
        for number in _LINK_NUMBERS
        if openupgrade.column_exists(env.cr, _TABLE, "link_%d_id" % number)
    ]
    openupgrade.drop_columns(env.cr, columns)
    _logger.info("Dropped %s old Link column(s) of %s.", len(columns), _TABLE)
