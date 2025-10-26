# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSbb33b94(models.Model):
    _name = "general_audit_ws_bb33b94"
    _description = "Final Materiality (bb33b94)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_final_materiality." "worksheet_type_bb33b94"
    )

    ws_d9d2b44_id = fields.Many2one(
        comodel_name="general_audit_ws_d9d2b44",
        string="# Preliminary Materiality",
        ondelete="restrict",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        related="ws_d9d2b44_id.computation_item_id",
        readonly=True,
        store=True,
    )
    general_audit_computation_id = fields.Many2one(
        string="General Audit Computation",
        related="ws_d9d2b44_id.general_audit_computation_id",
        readonly=True,
        store=True,
    )
    other_amount_ok = fields.Boolean(
        string="Use Other Amount",
        related="ws_d9d2b44_id.other_amount_ok",
        readonly=True,
        store=True,
    )
    other_amount_source = fields.Char(
        string="Other Amount Source",
        related="ws_d9d2b44_id.other_amount_source",
        readonly=True,
        store=True,
    )
    other_base_amount = fields.Monetary(
        string="Other Base Amount",
        related="ws_d9d2b44_id.other_base_amount",
        readonly=True,
        store=True,
    )

    # Base Amount
    planning_base_amount = fields.Monetary(
        string="Planning Base Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )
    audited_base_amount = fields.Monetary(
        string="Audited Base Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )
    unaudited_base_amount = fields.Monetary(
        string="Unaudited Base Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )

    overall_materiality_percentage = fields.Float(
        string="Overall Materiality Percentage (%)",
        realated="ws_d9d2b44_id.overall_materiality_percentage",
        readonly=True,
        store=True,
    )
    performance_materiality_percentage = fields.Float(
        string="Performance Materiality Percentage (%)",
        related="ws_d9d2b44_id.performance_materiality_percentage",
        readonly=True,
        store=True,
    )
    tolerable_misstatement_percentage = fields.Float(
        string="Tolerable Misstatement Percentage (%)",
        related="ws_d9d2b44_id.tolerable_misstatement_percentage",
        readonly=True,
        store=True,
    )

    def _compute_amount(self):
        for record in self:
            planning_base_amount = unaudited_base_amount = audited_base_amount = 0.0
            record.planning_base_amount = planning_base_amount
            record.audited_base_amount = audited_base_amount
            record.unaudited_base_amount = unaudited_base_amount
