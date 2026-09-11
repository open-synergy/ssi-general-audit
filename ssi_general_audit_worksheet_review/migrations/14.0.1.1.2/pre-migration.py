# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
#
# Migration: 14.0.1.1.1 -> 14.0.1.1.2
#
# Changes: general_audit_ws_a025441 no longer inherits mixin.checklist --
#          it now stores the completed disclosure checklist as CSV in the
#          new raw_data field. The item master
#          (general_audit_ws_a025441.item) and checklist value model
#          (general_audit_ws_a025441.checklist) are removed from the
#          code entirely (GitHub issue #326). By the time this
#          pre-migration script runs, the Python classes for both models
#          are already gone from the registry, so ir.model.unlink() is
#          not available for them: it raises for state='base' models,
#          which is exactly why a plain code removal never cleans up
#          the orphaned ir.model/ir.model.fields rows on its own (see
#          odoo-development skill, 10-migration-script.md §5). This
#          script deletes those two rows with a raw SQL statement,
#          bypassing that Python-level restriction entirely.
#
#          ir.model.fields.model_id and ir.model.access.model_id are
#          both declared ondelete='cascade' onto ir.model
#          (odoo/addons/base/models/ir_model.py:475, :1700), so deleting
#          ir.model rows cascades their field/access rows at the
#          Postgres FK level -- no separate DELETE needed for those.
#          ir.ui.view/ir.actions.act_window/ir.ui.menu are left alone on
#          purpose: their XML declarations were removed from this
#          module's data list, so Odoo's own orphaned-ir.model.data
#          cleanup at the end of the upgrade (_process_end) unlinks them
#          safely on its own -- neither model carries the state='base'
#          restriction. Manually deleting ir.model.data rows by a
#          name-prefix pattern was tried and reverted: a
#          'general_audit_ws_a025441_item%' wildcard also matches the
#          UNRELATED, KEPT general_audit_ws_a025441_item_group
#          res.groups record (still referenced by
#          ssi_general_audit_core/security/res_groups/
#          system_administrator.xml), silently orphaning it and making
#          the next -u fail with "duplicate key value violates unique
#          constraint res_groups_name_uniq" when Odoo tried to
#          re-create it -- caught locally while testing this migration
#          against a database where the module was already installed.
#
#          general_audit_ws_a025441_checklist.item_id carries a foreign
#          key onto general_audit_ws_a025441_item, so the checklist
#          table is dropped before the item table.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_MODELS = [
    "general_audit_ws_a025441.checklist",
    "general_audit_ws_a025441.item",
]


@openupgrade.migrate()
def migrate(env, version):
    """Purge the general_audit_ws_a025441 checklist/item models.

    Deletes the ir.model rows for ``general_audit_ws_a025441.checklist``
    and ``general_audit_ws_a025441.item`` (cascading their
    ir.model.fields and ir.model.access rows), then drops their tables.
    Every other object (views, action, menu, and their ir.model.data
    entries) is left for Odoo's own orphaned-data cleanup, since none
    of those models carry the state='base' restriction that blocks it.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes rows and drops tables for the two
        removed models
    """
    cr = env.cr

    # ir.model -- cascades ir.model.fields and ir.model.access via their
    # ondelete='cascade' foreign key onto ir_model.id.
    rows = openupgrade.logged_query(
        cr,
        "DELETE FROM ir_model WHERE model IN %s",
        (tuple(_MODELS),),
    )
    _logger.info("Removed %s ir.model row(s) (cascades fields/access).", rows)

    # Drop the tables. The checklist table's item_id column carries a
    # foreign key onto general_audit_ws_a025441_item, so it MUST be
    # dropped first -- dropping the item table first raises
    # psycopg2.errors.DependentObjectsStillExist and rolls back the
    # whole migration (odoo-development skill, 10-migration-script.md
    # §5, §5a). Neither table is the target of a many2many relation
    # table of its own.
    openupgrade.logged_query(
        cr, "DROP TABLE IF EXISTS general_audit_ws_a025441_checklist"
    )
    openupgrade.logged_query(cr, "DROP TABLE IF EXISTS general_audit_ws_a025441_item")
