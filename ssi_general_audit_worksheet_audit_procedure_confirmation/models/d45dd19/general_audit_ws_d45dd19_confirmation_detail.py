# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSd45dd19ConfirmationDetail(models.Model):
    """
    Detail line for a Confirmation record of WS-D45DD19.

    Each line represents one reference item included in the parent confirmation
    request.  The auditor specifies which column in the linked raw data
    identifies the item (``ref_col_number`` / ``ref_value``), records the book
    balance and the amount confirmed by the external party, and the system
    derives the confirmation status automatically.

    **ISA / SA references:** ISA 505 / SA 505 — External Confirmations.
    """

    _name = "general_audit_ws_d45dd19.confirmation.detail"
    _description = "Confirmation Audit Procedure WS - Confirmation Detail"
    _order = "confirmation_id, sequence, id"

    confirmation_id = fields.Many2one(
        comodel_name="general_audit_ws_d45dd19.confirmation",
        string="Confirmation",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    ref_col_number = fields.Integer(
        string="Ref Column Number",
        help="Column number (1-based) in the linked raw data that contains "
        "the reference identifier for this item (e.g. account number column).",
    )
    ref_value = fields.Char(
        string="Reference Value",
        help="The reference identifier for this item (e.g. account number). "
        "Entered manually or derived from the raw data column above.",
    )
    book_amount = fields.Float(
        string="Book Amount (IDR)",
        digits=(16, 2),
        help="Book balance in IDR as recorded in the client's books for this "
        "reference item.",
    )
    confirmation_amount = fields.Float(
        string="Confirmation Amount (IDR)",
        digits=(16, 2),
        help="Amount confirmed by the external party in IDR for this reference "
        "item.",
    )
    diff = fields.Float(
        string="Difference",
        digits=(16, 2),
        compute="_compute_diff",
        store=True,
        help="Difference between the book amount and the confirmed amount.  "
        "Zero means the confirmation agrees with the books.",
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ("agreed", "Agreed"),
            ("different", "Different"),
        ],
        compute="_compute_status",
        store=True,
        help="Confirmation status derived automatically from the difference: "
        "'Agreed' when diff = 0, 'Different' otherwise.",
    )

    @api.depends("book_amount", "confirmation_amount")
    def _compute_diff(self):
        for record in self:
            record.diff = record.book_amount - record.confirmation_amount

    @api.depends("diff")
    def _compute_status(self):
        for record in self:
            record.status = "agreed" if record.diff == 0.0 else "different"
