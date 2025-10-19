# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSe51bb1c(models.Model):
    _name = "general_audit_ws_e51bb1c"
    _description = "Key Audit Procedures (e51bb1c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_lead_schedule." "worksheet_type_e51bb1c"

    account_type_id = fields.Many2one(
        comodel_name="client_account_type",
        string="Standard Account",
        required=True,
        states={
            "draft": [("readonly", False)],
        },
        readonly=True,
        ondelete="restrict",
    )
    allowed_account_type_ids = fields.Many2many(
        comodel_name="client_account_type",
        string="Allowed Account Types",
        help="Account types that can be selected",
        compute="_compute_allowed_account_type_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_e51bb1c.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
    )

    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_account_type_ids(self):
        for record in self:
            record.allowed_account_type_ids = self.env["client_account_type"]
            if record.general_audit_id:
                record.allowed_account_type_ids = record.general_audit_id.mapped(
                    "standard_detail_ids.type_id"
                )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        detail_obj = self.env["general_audit_ws_e51bb1c.detail"]
        procedure_domain = [
            ("account_type_id", "=", self.account_type_id.id),
        ]

        all_procedures = self.env["general_audit_audit_procedure"].search(
            procedure_domain
        )
        existing_procedure_ids = self.detail_ids.mapped("audit_procedure_id")

        to_be_added_procedures = all_procedures - existing_procedure_ids
        to_be_remove_procedures = existing_procedure_ids - all_procedures

        for procedure in to_be_added_procedures:
            detail_obj.create(
                {
                    "worksheet_id": self.id,
                    "audit_procedure_id": procedure.id,
                    "assertion_type_ids": [
                        (6, 0, [procedure.category_id.assertion_type_ids.ids])
                    ],
                }
            )

        to_be_removed_details = self.detail_ids.filtered(
            lambda d: d.audit_procedure_id in to_be_remove_procedures
        )
        if to_be_removed_details:
            to_be_removed_details.sudo().unlink()
