# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.0 -> 14.0.1.2.0
#
# Changes: the seed templates and columns moved from a noupdate data
#          file to an updatable one. The ir.model.data rows already
#          carry noupdate = true, and Odoo skips such rows even when
#          the XML file is no longer noupdate, so they are reset here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Make the seed templates and columns updatable again.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``ir_model_data`` rows
    """
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_data
        SET noupdate = false
        WHERE module = %s
            AND model IN %s
            AND noupdate IS TRUE
        """,
        (
            "ssi_general_audit_import_template",
            (
                "general_audit_import_template",
                "general_audit_import_template.line",
            ),
        ),
    )
    _logger.info("Reset noupdate on %s seed xmlid(s).", rows)
