# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditWSA3C9D2E(models.Model):
    _name = "general_audit_ws_a3c9d2e"
    _description = "Analytical Procedures – Cycle (a3c9d2e)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_audit_procedure_analytic_cycle"
        ".worksheet_type_a3c9d2e"
    )
