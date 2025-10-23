# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSd33420f(models.Model):
    _name = "general_audit_ws_d33420f"
    _description = "Control Deficiencies (d33420f)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_d33420f"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_d33420f.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "List of control deficiency detail lines captured in this worksheet. "
            "Editable when the worksheet is in the 'Open' state."
        ),
    )
