# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScb82c5fNonAdjustmentDetail(models.Model):
    _name = "general_audit_ws_cb82c5f.non_adjustment_detail"
    _description = "Subsequent Event (cb82c5f) - Non Adjustment Detail"

    worksheet_id = fields.Many2one(
        comodel_name="general_audit_ws_cb82c5f",
        string="Worksheet",
        required=True,
        ondelete="cascade",
        help="Parent Subsequent Event worksheet for this non-adjustment detail line.",
    )
    subsequent_event_id = fields.Many2one(
        comodel_name="general_audit_subsequent_event",
        string="Subsequent Event",
        required=True,
        help="Subsequent event ID",
    )
    occurance = fields.Selection(
        string="Occurance",
        selection=[
            ("occurred", "Occurred"),
            ("not_occurred", "Not Occurred"),
        ],
        required=True,
        default="not_occurred",
        help="Indicate whether the subsequent event has occurred or not",
    )
    to_disclose = fields.Selection(
        string="To Disclose",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        default="no",
        help="Indicate whether the subsequent event needs to be disclosed",
    )
    disclosure = fields.Text(
        string="Disclosure",
        help="Details of the disclosure for the subsequent event",
    )
    reference = fields.Char(
        string="Reference",
        help="Reference information related to the subsequent event",
    )
