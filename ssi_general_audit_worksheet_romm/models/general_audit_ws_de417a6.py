from odoo import fields, models


class GeneralAuditWSde417a6(models.Model):
    _name = "general_audit_ws_de417a6"
    _description = "General Audit Worksheet DE417A6"

    # ...existing fields...
    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de417a6.checklist",
        help=(
            "Checklist responses recorded for this worksheet; each line stores an "
            "answer for a checklist item."
        ),
    )
