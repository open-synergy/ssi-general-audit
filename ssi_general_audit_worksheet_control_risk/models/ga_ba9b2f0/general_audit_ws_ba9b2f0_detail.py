# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSba9b2f0Detail(models.Model):
    _name = "general_audit_ws_ba9b2f0.detail"
    _description = "Worksheet ba9b2f0 - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ba9b2f0",
        required=True,
        ondelete="cascade",
        help="Parent worksheet this line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Ordering number used to sort lines; lower values appear first.",
    )
    key_internal_control_id = fields.Many2one(
        string="Key Internal Control",
        comodel_name="general_audit_account_key_internal_control",
        required=True,
        ondelete="restrict",
        help="Selected key internal control related to the standard account.",
    )
    name = fields.Char(
        string="Description",
        required=True,
        help="Short description of the control activity.",
    )
    frequency = fields.Char(
        string="Frequency",
        required=True,
        help=(
            "How often the control operates (e.g., daily, weekly, monthly, per "
            "transaction)."
        ),
    )
    risk_identification_ids = fields.One2many(
        string="Risk Identifications",
        comodel_name="general_audit_ws_ba9b2f0.risk_identification",
        inverse_name="detail_id",
        help="Identified risks associated with this control.",
    )
    what_can_go_wrong_ids = fields.One2many(
        string="What Can Go Wrong",
        comodel_name="general_audit_ws_ba9b2f0.what_can_go_wrong",
        inverse_name="detail_id",
        help=(
            "Potential failure scenarios describing what could go wrong with the "
            "control."
        ),
    )
    documentation = fields.Text(
        string="Documentation",
        required=False,
        help=(
            "Supporting evidence or references (e.g., policies, procedures, "
            "screenshots, logs)."
        ),
    )
    rely_on_control = fields.Selection(
        string="Rely on COntrol",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        required=True,
        help=(
            "Indicate whether the audit approach intends to rely on this control "
            "for reducing substantive testing."
        ),
    )
    toc_analysis = fields.Selection(
        string="ToC Analysis",
        selection=[
            ("effective", "Effective"),
            ("not_effective", "Not Effective"),
            ("na", "N/A"),
        ],
        required=True,
        help="Assessment result from Test of Controls (ToC).",
    )
    toc_reference = fields.Char(
        string="ToC Reference",
        help="Reference to ToC workpapers, procedures, or evidence.",
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("high", "High"),
            ("low", "Low"),
        ],
        compute="_compute_result",
        store=True,
        compute_sudo=True,
        help=(
            "Computed control risk result. It becomes 'low' only when "
            "rely_on_control is 'yes' and ToC analysis is 'effective'; otherwise "
            "it is 'high'."
        ),
    )

    @api.depends(
        "rely_on_control",
        "toc_analysis",
    )
    def _compute_result(self):
        for record in self:
            if record.rely_on_control == "yes" and record.toc_analysis == "effective":
                result = "low"
            else:
                result = "high"
            record.result = result
