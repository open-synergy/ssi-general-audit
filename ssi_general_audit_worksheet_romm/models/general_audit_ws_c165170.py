# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc165170(models.Model):
    """
    WS: Financial Statement Level ROMM (c165170) — ISA 315 / SA 315.

    Documents the auditor's **financial statement-level risk of material
    misstatement** assessment by aggregating risk information from multiple
    upstream risk-assessment worksheets.  This worksheet is reviewed by the
    Engagement Partner to confirm the overall engagement risk profile and
    to determine whether the planned audit approach appropriately addresses
    identified financial statement-level risks.

    Linked upstream worksheets:

    * ``ws_c0e0eec_id`` — Fraud Factor Analysis.
    * ``ws_b59b886_id`` — Control Risk – Entity Level.
    * ``ws_f6a227_id``  — Understanding of Financial Statement Preparation.

    The worksheet carries forward review notes from each linked worksheet and
    adds the auditor's overall financial statement-level ROMM narrative and
    the planned audit responses at the financial statement level (e.g.,
    assigning more experienced staff, emphasising professional scepticism,
    applying element of unpredictability).
    """

    _name = "general_audit_ws_c165170"
    _description = "Financial Level ROMM (c165170)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_c165170"

    # Link

    ws_c0e0eec_id = fields.Many2one(
        string="# Fraud Factor Analysis",
        comodel_name="general_audit_ws_c0e0eec",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        ondelete="restrict",
        help="Link to Fraud Factor Analysis worksheet.",
    )
    ws_c0e0eec_id_review = fields.Text(
        string="Review Note on Fraud Factor Analysis",
        related="ws_c0e0eec_id.review",
        readonly=True,
        help="Review note from the linked Fraud Factor Analysis worksheet.",
    )
    ws_b59b886_id = fields.Many2one(
        string="# Control Risk - Entity Level",
        comodel_name="general_audit_ws_b59b886",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        ondelete="restrict",
        help="Link to Control Risk - Entity Level worksheet.",
    )
    ws_f6a227_id = fields.Many2one(
        string="# Understanding of preparation of Financial Statements",
        comodel_name="general_audit_ws_f6a227",
        readonly=True,
        required=False,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    ws_f6a227_id_review = fields.Text(
        related="ws_f6a227_id.review",
        string="Review Note on Understanding of preparation of Financial Statements",
        readonly=True,
    )
    ws_b59b886_id_review = fields.Text(
        string="Review Note on Control Risk - Entity Level",
        related="ws_b59b886_id.review",
        readonly=True,
        help="Review note from the linked Control Risk - Entity Level worksheet.",
    )
    ws_bdcdfc5_ids = fields.Many2many(
        string="# Understanding of the Business Environment",
        comodel_name="general_audit_ws_bdcdfc5",
        relation="general_audit_ws_c165170_bdcdfc5_rel",
        column1="ws_c165170_id",
        column2="ws_bdcdfc5_id",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help="Links to Understanding of the Business Environment worksheets.",
    )

    risk_material_missstatement = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Overall financial statement-level risk of material misstatement (ROMM) "
            "assessment for this worksheet."
        ),
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Summary of the auditor's planned overall responses at the financial "
            "statement level to address the assessed ROMM."
        ),
    )
