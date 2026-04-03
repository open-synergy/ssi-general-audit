# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditAuditProcedureCategory(models.Model):
    """
    Master: Audit Procedure Category.

    Represents a **logical grouping of audit procedures** for a specific
    account type and set of assertion types.  For example:
    *"Existence and Occurrence – Accounts Receivable"*.

    Each category is linked to:

    * ``account_type_id`` — the account type to which the procedures apply.
    * ``assertion_type_ids`` — the assertion types addressed (existence,
      completeness, accuracy, cut-off, classification, presentation, etc.).
    * ``step_ids`` — the individual procedure steps (``general_audit_audit_procedure``)
      that belong to this category.

    Categories form the **library** from which the Key Audit Procedures
    worksheet (``general_audit_ws_e51bb1c``) is populated when the auditor
    calls *Load Detail*.
    """

    _name = "general_audit_audit_procedure_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Key Audit Procedure"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Account Type",
        required=True,
        ondelete="restrict",
    )
    assertion_type_ids = fields.Many2many(
        comodel_name="general_audit_assersion_type",
        string="Applicable Assertions",
        required=True,
        relation="rel_audit_procedure_category_2_assertion_type",
        column1="category_id",
        column2="assertion_type_id",
    )
    step_ids = fields.One2many(
        comodel_name="general_audit_audit_procedure",
        inverse_name="category_id",
        string="Audit Procedure Steps",
        help="List of audit procedure steps under this category.",
    )
