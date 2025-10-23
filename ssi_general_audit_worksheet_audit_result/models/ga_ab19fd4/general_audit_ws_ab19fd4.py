# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSab19fd4(models.Model):
    _name = "general_audit_ws_ab19fd4"
    _description = "Audit Result Formulation (ab19fd4)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_ab19fd4"

    # Findings That Influence Opinion
    # LINK - 1 a0319a2 (WR. 110.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a0319a2"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.detail_ids.ids
            record.link_1_ids = result

    link_1_ids = fields.Many2many(
        string="WR. 110.1",
        comodel_name="general_audit_ws_a0319a2.detail",
        compute_sudo=True,
        compute="_compute_link_1_ids",
        store=True,
        help=(
            "Auto-populated link to 'Findings That Influence Opinion' (WR. 110.1). "
            "Computed from worksheet a0319a2 belonging to the same general audit."
        ),
    )

    # Control Deficiencies
    # LINK - 2 d33420f (WR. 110.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d33420f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.detail_ids.ids
            record.link_2_ids = result

    link_2_ids = fields.Many2many(
        string="WR. 110.2",
        comodel_name="general_audit_ws_d33420f.detail",
        compute_sudo=True,
        compute="_compute_link_2_ids",
        store=True,
        help=(
            "Auto-populated link to 'Control Deficiencies' (WR. 110.2). "
            "Computed from worksheet d33420f belonging to the same general audit."
        ),
    )

    def action_recompute(self):
        for record in self:
            record._compute_link_1_ids()
            record._compute_link_2_ids()
