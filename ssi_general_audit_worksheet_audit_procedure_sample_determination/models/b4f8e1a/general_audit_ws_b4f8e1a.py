# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditWSB4F8E1A(models.Model):
    _name = "general_audit_ws_b4f8e1a"
    _description = "Sample Determination (b4f8e1a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_sample_determination"
        ".worksheet_type_b4f8e1a"
    )
