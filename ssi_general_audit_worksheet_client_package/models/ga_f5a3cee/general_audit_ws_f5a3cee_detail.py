# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWSf5a3ceeDetail(models.Model):
    """Detail line for the Data Collection worksheet (f5a3cee).

    Groups the data requested for one client account type.  The collected
    data itself is tracked on ``line_ids``, one line per Data Collection
    master item of that account type.
    """

    _name = "general_audit_ws_f5a3cee.detail"
    _description = "Data Collection (f5a3cee) - Details"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5a3cee",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Data Collection worksheet. "
            "Deleting the worksheet will remove its details."
        ),
    )
    account_client_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        required=True,
        ondelete="restrict",
        help="Client account type that this detail line refers to.",
    )
    line_ids = fields.One2many(
        string="Data Collection",
        comodel_name="general_audit_ws_f5a3cee.detail_line",
        inverse_name="detail_id",
        help="Data requested for this account type, taken from the master.",
    )
    line_count = fields.Integer(
        string="Lines",
        compute="_compute_line_count",
        store=True,
        help="Number of data lines of this detail.",
    )
    line_done_count = fields.Float(
        string="Completed Lines",
        compute="_compute_line_done_count",
        store=True,
        help="Number of completed data lines of this detail.",
    )
    complete_ok = fields.Boolean(
        string="Completed",
        compute="_compute_complete_ok",
        store=True,
        help=(
            "Checked automatically when the detail has data lines and all "
            "of them are completed."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )

    @api.depends("line_ids")
    def _compute_line_count(self):
        """Count the data lines of the detail."""
        for record in self:
            result = len(record.line_ids)
            record.line_count = result

    @api.depends("line_ids.complete_ok")
    def _compute_line_done_count(self):
        """Count the completed data lines of the detail."""
        for record in self:
            result = len(record.line_ids.filtered("complete_ok"))
            record.line_done_count = result

    @api.depends("line_ids.complete_ok")
    def _compute_complete_ok(self):
        """Compute whether every data line of the detail is completed."""
        for record in self:
            result = bool(record.line_ids) and all(
                record.line_ids.mapped("complete_ok")
            )
            record.complete_ok = result

    @api.constrains("worksheet_id", "account_client_type_id")
    def _check_duplicate_account_type(self):
        """Reject a repeated account type in one worksheet.

        :raises ValidationError: if another detail of the same worksheet
            has the same account type.
        """
        for record in self:
            siblings = record.worksheet_id.detail_ids - record
            if record.account_client_type_id in siblings.account_client_type_id:
                raise ValidationError(
                    _("Account type %s is already used in this worksheet.")
                    % record.account_client_type_id.name
                )
