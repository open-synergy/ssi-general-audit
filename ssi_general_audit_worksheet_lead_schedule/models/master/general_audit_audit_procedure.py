# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditAuditProcedure(models.Model):
    """
    Master: Audit Procedure Step.

    Represents a **single, executable audit procedure step** within a procedure
    category.  Examples: *"Trace cash receipts to bank statement"*,
    *"Confirm accounts receivable balances with customers"*.

    Fields:

    * ``account_type_id`` — the account type to which this step applies (also
      used to filter the ``category_id`` domain on the form view).
    * ``category_id`` — the parent procedure category
      (``general_audit_audit_procedure_category``).

    Steps are referenced from procedure category lines and are included in the
    Key Audit Procedures worksheet detail when *Load Detail* is executed.
    """

    _name = "general_audit_audit_procedure"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Key Audit Procedure Steps"

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
    category_id = fields.Many2one(
        comodel_name="general_audit_audit_procedure_category",
        string="Category",
        required=True,
        ondelete="restrict",
    )

    @api.onchange("account_type_id")
    def onchange_category_id(self):
        self.category_id = False
