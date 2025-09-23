# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    audit_ok = fields.Boolean(
        string="Can Audit",
        default=False,
        help="If checked, this employee can audit.",
    )
