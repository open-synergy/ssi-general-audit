# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.3.1 -> 14.0.1.4.0
#
# Changes: the Test of Detail Planning worksheet is rewritten as one line
#          per standard account. The old header columns (sampling,
#          confidence factor, materiality, ...) are gone and the lines
#          are rebuilt with the Detail button. The old line table has
#          required columns that no longer exist, so this script drops
#          it and the ORM recreates it. Header columns removed from the
#          model are dropped here because Odoo leaves them in place.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_HEADER_TABLE = "general_audit_ws_f9a2c3d"
_DETAIL_TABLE = "general_audit_ws_f9a2c3d_detail"

_OLD_HEADER_COLUMNS = (
    "standard_detail_id",
    "account_type_id",
    "materiality",
    "romm",
    "significant_account",
    "specific_materiality",
    "risk_factor_adjustment",
    "preliminary_materiality_id",
    "performance_materiality",
    "need_ap",
    "ap_result",
    "need_tod",
    "timing",
    "direct_examination",
    "need_sampling",
    "tod_level",
    "audited_balance",
    "key_item_amount",
    "sampling_amount",
    "confidence_factor",
    "sampling_interval",
    "sample_count",
)


@openupgrade.migrate()
def migrate(env, version):
    """Drop the old line table and the removed header columns.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; drops the old detail table and header columns
    """
    cr = env.cr
    if openupgrade.table_exists(cr, _DETAIL_TABLE):
        openupgrade.logged_query(cr, "DROP TABLE %s" % _DETAIL_TABLE)
    columns = [
        (_HEADER_TABLE, column)
        for column in _OLD_HEADER_COLUMNS
        if openupgrade.column_exists(cr, _HEADER_TABLE, column)
    ]
    openupgrade.drop_columns(cr, columns)
    _logger.info(
        "Dropped %s old header column(s) of %s and the table %s.",
        len(columns),
        _HEADER_TABLE,
        _DETAIL_TABLE,
    )
