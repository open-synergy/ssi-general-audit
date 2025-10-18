from odoo import fields, models


class GeneralAuditWSde417a6Item(models.Model):
    _name = "general.audit.ws.de417a6.item"
    _description = "General Audit WS de417a6 Item"

    # ...existing fields...
    code = fields.Char(
        default="/",
        help=(
            "Optional code for the checklist item. Use '/' to auto-generate or allow the "
            "system to assign a reference."
        ),
    )
