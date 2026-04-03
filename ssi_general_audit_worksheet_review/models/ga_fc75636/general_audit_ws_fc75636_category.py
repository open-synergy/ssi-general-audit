# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSfc75636Category(models.Model):
    """
    Master: Independent Auditor's Report Section Category (fc75636).

    Provides a configurable category hierarchy used to group items in
    the Independent Auditor's Report Review checklist (fc75636) by report
    section.  Examples: *Report Title*, *Addressee*, *Basis for Opinion*,
    *Key Audit Matters*, *Management Responsibility*, *Auditor's
    Responsibility*, *Opinion paragraph*.
    """

    _name = "general_audit_ws_fc75636.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Independen Auditor Report (fc75636) - " "Category"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
