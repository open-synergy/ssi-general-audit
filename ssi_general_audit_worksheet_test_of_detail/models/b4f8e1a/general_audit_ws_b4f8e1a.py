# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class GeneralAuditWsB4f8e1a(models.Model):
    """
    Test of Detail worksheet: records the substantive test result for each
    item selected by the corresponding Sample Determination worksheet.
    """

    _name = "general_audit_ws_b4f8e1a"
    _description = "Test of Detail (b4f8e1a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_test_of_detail" ".worksheet_type_b4f8e1a"
    )
