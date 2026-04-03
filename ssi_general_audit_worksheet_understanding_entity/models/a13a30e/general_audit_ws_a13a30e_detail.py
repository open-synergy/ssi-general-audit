# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSa13a30eOrganizationStructure(models.Model):
    """Regulation detail line within the Relevant Regulations worksheet.

    Records a specific regulation and item/section applicable to the audit
    entity. Each line links the regulation to affected standard account types
    and flags whether the regulation has significant impact on the financial
    statements. This enables auditors to trace regulatory requirements to
    specific audit areas and design compliance-focused procedures (ISA 250).
    """

    _name = "general_audit_ws_a13a30e.detail"
    _description = "Worksheet a13a30e - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a13a30e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This detail will be removed if the worksheet is deleted."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Ordering of this line within the worksheet.",
    )
    regulation_id = fields.Many2one(
        string="Regulation",
        comodel_name="general_audit_relevant_regulation",
        required=True,
        ondelete="restrict",
        help="Relevant regulation or law applicable to the entity.",
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="general_audit_relevant_regulation.item",
        required=True,
        ondelete="restrict",
        help="Specific item/section of the regulation being tracked.",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_a13a30e_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this regulation. Used to link the item "
            "to relevant accounts."
        ),
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_a13a30e_detail_2_standard_detail",
        column1="detail_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
        help=(
            "Standard details automatically linked based on the selected account types "
            "and the worksheet's General Audit."
        ),
    )
    significant_impact = fields.Boolean(
        string="Significant Impact",
        default=False,
        help=(
            "Indicates whether this regulation has a significant impact on the financial "
            "statements or disclosures."
        ),
    )

    @api.depends(
        "related_account_type_ids",
    )
    def _compute_standard_detail_ids(self):
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            general_audit = record.worksheet_id.general_audit_id
            criteria = [
                ("general_audit_id", "=", general_audit.id),
                ("type_id", "in", record.related_account_type_ids.ids),
            ]
            standard_details = StandardDetail.search(criteria)
            if len(standard_details) > 0:
                result = standard_details.ids
            record.standard_detail_ids = result
