# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSb9d8a5c(models.Model):
    _name = "general_audit_ws_b9d8a5c"
    _description = (
        "Competency, Availability and Independency " "Of Assignment Team (b9d8a5c)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_b9d8a5c"
    )
