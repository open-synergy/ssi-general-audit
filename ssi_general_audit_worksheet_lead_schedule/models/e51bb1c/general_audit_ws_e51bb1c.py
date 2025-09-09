# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSe51bb1c(models.Model):
    _name = "general_audit_ws_e51bb1c"
    _description = "Key Audit Procedures (e51bb1c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_e51bb1c"
