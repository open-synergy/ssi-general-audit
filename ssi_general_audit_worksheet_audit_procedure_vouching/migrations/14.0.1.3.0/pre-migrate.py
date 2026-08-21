# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
#
# Migration: 14.0.1.2.0 -> 14.0.1.3.0
#
# Changes: general_audit_ws_b4f7d9c.test_of_detail_id was mislabeled --
#          it points at general_audit_ws_a916660, which is the Sample
#          Determination worksheet (see the sibling identity swap of
#          ssi_general_audit_worksheet_test_of_detail <->
#          ssi_general_audit_worksheet_sample_determination), not Test of
#          Detail. The field is renamed to sample_determination_id in
#          code; rename the underlying column in place so existing data
#          is preserved instead of the column being dropped and recreated
#          empty.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Rename the test_of_detail_id column to sample_determination_id.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; renames a column on ``general_audit_ws_b4f7d9c``
    """
    if not openupgrade.column_exists(
        env.cr, "general_audit_ws_b4f7d9c", "test_of_detail_id"
    ):
        _logger.info("test_of_detail_id column not found, nothing to rename.")
        return

    openupgrade.rename_columns(
        env.cr,
        {
            "general_audit_ws_b4f7d9c": [
                ("test_of_detail_id", "sample_determination_id"),
            ],
        },
    )
