# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.11.2 -> 14.0.1.12.0
#
# Changes: the stored Many2many ``link_27_ids`` (Population) was
#          removed from ``general_audit_ws_a8c54f3``. The field is
#          dropped by the ORM, but its relation table is not, so the
#          table is dropped here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

RELATION_TABLE = "general_audit_ws_a01723b_general_audit_ws_a8c54f3_rel"


@openupgrade.migrate()
def migrate(env, version):
    """Drop the relation table of the removed ``link_27_ids`` field.

    The script is idempotent: it does nothing when the table is gone.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; drops the relation table
    """
    openupgrade.logged_query(
        env.cr,
        'DROP TABLE IF EXISTS "%s"' % RELATION_TABLE,
    )
    _logger.info("Dropped relation table %s.", RELATION_TABLE)
