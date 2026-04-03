# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7ESupplier(models.Model):
    """Key supplier entry within the Main Business Activity worksheet.

    Records significant suppliers of the entity, their total purchase value,
    and the percentage they represent of total procurement. Supplier
    concentration and dependence information supports the auditor's assessment
    of supply chain risks and the going concern evaluation (ISA 315, ISA 570).
    """

    _name = "general_audit_ws_ae11f7e.supplier"
    _description = "Worksheet ae11f7e - Supplier"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This supplier entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        string="Supplier",
        required=True,
        help="Supplier name.",
    )
    value = fields.Float(
        required=True,
        help="Total purchases from this supplier for the period (company currency).",
    )
    percentage = fields.Float(
        string="From Purchases",
        required=True,
        help="Percentage of total purchases attributable to this supplier.",
    )
