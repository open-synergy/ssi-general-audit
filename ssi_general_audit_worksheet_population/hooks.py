# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import SUPERUSER_ID, api

WORKSHEET_TYPE_XMLID = "ssi_general_audit_worksheet_population.worksheet_type_a01723b"
WORKSHEET_TYPE_MODEL = "general_audit_worksheet_type"


def _clean_references(env, worksheet_type):
    """Remove every record that still points to the given worksheet type.

    References are discovered through ``ir.model.fields`` so that links
    added by other modules are handled too. Only records pointing to
    ``worksheet_type`` are touched.

    :param env: superuser environment.
    :param worksheet_type: ``general_audit_worksheet_type`` record.
    """
    fields_ = env["ir.model.fields"].search(
        [
            ("relation", "=", WORKSHEET_TYPE_MODEL),
            ("store", "=", True),
            ("ttype", "in", ["many2one", "many2many"]),
        ]
    )
    for field_info in fields_:
        if field_info.model not in env.registry:
            continue
        model = env[field_info.model]
        field = model._fields.get(field_info.name)
        if model._abstract or field is None or not field.store:
            continue
        records = model.with_context(active_test=False).search(
            [(field.name, "=", worksheet_type.id)]
        )
        if not records:
            continue
        if field.type == "many2many":
            records.write({field.name: [(3, worksheet_type.id)]})
        elif field_info.model == WORKSHEET_TYPE_MODEL:
            # Self reference (parent): detach instead of deleting.
            records.write({field.name: False})
        else:
            records.unlink()


def uninstall_hook(cr, registry):
    """Delete the Population worksheet type and everything referencing it.

    Odoo runs this hook before the module data (external identifiers)
    is removed, so the type is still reachable through its xmlid. The
    hook is idempotent: it does nothing when the type is already gone.

    :param cr: database cursor.
    :param registry: model registry of the database.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    worksheet_type = env.ref(WORKSHEET_TYPE_XMLID, raise_if_not_found=False)
    if not worksheet_type or not worksheet_type.exists():
        return
    _clean_references(env, worksheet_type)
    worksheet_type.unlink()
