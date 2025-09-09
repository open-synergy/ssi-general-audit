# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSc2375d8(models.Model):
    _name = "general_audit_ws_c2375d8"
    _description = "Final Analytical Procedures (c2375d8)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_c2375d8"
    )
