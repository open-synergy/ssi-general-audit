# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWSbb33b94(models.Model):
    _name = "general_audit_ws_bb33b94"
    _description = "Final Materiality (bb33b94)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_bb33b94"
    )
