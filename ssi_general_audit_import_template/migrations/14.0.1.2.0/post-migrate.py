# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.0 -> 14.0.1.2.0
#
# Changes: the name of a download server action now follows the name
#          of its template, but server actions created before this version
#          kept the name they got at creation, so they are aligned.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Align the server action names with their template names.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``ir_act_server`` rows
    """
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_act_server AS act
        SET name = %s || tpl.name
        FROM general_audit_import_template AS tpl
        WHERE tpl.server_action_id = act.id
            AND act.name IS DISTINCT FROM %s || tpl.name
        """,
        ("Download Template: ", "Download Template: "),
    )
    _logger.info("Renamed %s download server action(s).", rows)
