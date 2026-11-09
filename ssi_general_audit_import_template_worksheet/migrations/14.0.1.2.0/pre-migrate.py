# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.1 -> 14.0.1.2.0
#
# Changes: the Population seed template is no longer shipped. Its
#          records are removed from existing databases, together with
#          the download server action a user may have created for it
#          (that action has no xmlid, so the data reload never drops it).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODULE = "ssi_general_audit_import_template_worksheet"
TEMPLATE = "general_audit_import_template_population"
LINES = [TEMPLATE + "_line_%s" % i for i in range(1, 5)]


@openupgrade.migrate()
def migrate(env, version):
    """Remove the Population seed template and its server action.

    The script is idempotent: it does nothing when the seed is gone.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes the seed template, columns and action
    """
    cr = env.cr
    cr.execute(
        "SELECT res_id FROM ir_model_data "
        "WHERE module = %s AND name = %s "
        "AND model = 'general_audit_import_template'",
        (MODULE, TEMPLATE),
    )
    row = cr.fetchone()
    if not row:
        _logger.info("No Population seed template found, nothing to do.")
        return
    cr.execute(
        "SELECT server_action_id FROM general_audit_import_template WHERE id = %s",
        (row[0],),
    )
    found = cr.fetchone()
    action_id = found and found[0]
    if action_id:
        # Unlinking the action also drops its Action menu binding.
        env["ir.actions.server"].browse(action_id).exists().unlink()
    openupgrade.delete_records_safely_by_xml_id(
        env, ["%s.%s" % (MODULE, name) for name in LINES + [TEMPLATE]]
    )
    _logger.info("Removed the Population seed template.")
