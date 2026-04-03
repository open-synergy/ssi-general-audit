# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbab9d32Factor(models.Model):
    """
    Auditor's Expert Worksheet — Evaluation Factor Master (bab9d32)

    Master-data model containing the library of evaluation factors for
    the Auditor's Expert worksheet (WS.040.1).  Examples of factors
    include: competence, capabilities, objectivity, scope adequacy.
    Factors are grouped by category and each is linked to exactly one
    ``general_audit_ws_bab9d32.category``.
    """

    _name = "general_audit_ws_bab9d32.factor"
    _inherit = [
        "mixin.expert.factor",
    ]
    _description = "Auditor Expert (bab9d32) - Factor"

    code = fields.Char(
        default="/",
        help="Internal code/identifier for the Expert Factor. Defaults to '/'.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_ws_bab9d32.category",
        required=True,
    )
