# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditWSC7D5F2B(models.Model):
    _name = "general_audit_ws_c7d5f2b"
    _description = "Inspection (c7d5f2b)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inspection.worksheet_type_c7d5f2b"
