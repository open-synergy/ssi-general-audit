# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7ECustomer(models.Model):
    """Key customer entry within the Main Business Activity worksheet.

    Records significant customers of the entity, their total sales value, and
    the percentage they represent of total revenues. Customer concentration
    information supports the auditor's risk assessment of revenue recognition
    and the going concern evaluation (ISA 315, ISA 570).
    """

    _name = "general_audit_ws_ae11f7e.customer"
    _description = "Worksheet ae11f7e - Customer"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This customer entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        string="Customer",
        required=True,
        help="Customer name.",
    )
    value = fields.Float(
        required=True,
        help="Total sales value to this customer for the period (company currency).",
    )
    percentage = fields.Float(
        string="From Sales",
        required=True,
        help="Percentage of total sales attributable to this customer.",
    )
