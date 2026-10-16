# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.0 -> 14.0.1.1.0
#
# Changes: the worksheet no longer stores the pre-tax impact, the
#          after-tax impact and the materiality conclusion; the aggregate
#          analysis replaces them. Odoo leaves the orphan columns behind,
#          so they are dropped here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_COLUMNS = [
    ("general_audit_ws_c3b9e71", "pre_tax_impact"),
    ("general_audit_ws_c3b9e71", "post_tax_impact"),
    ("general_audit_ws_c3b9e71", "materiality_conclusion"),
]


@openupgrade.migrate()
def migrate(env, version):
    """Drop the columns of the three removed fields.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; drops columns of ``general_audit_ws_c3b9e71``
    """
    openupgrade.drop_columns(env.cr, _COLUMNS)
    _logger.info("Dropped %s orphan column(s).", len(_COLUMNS))
