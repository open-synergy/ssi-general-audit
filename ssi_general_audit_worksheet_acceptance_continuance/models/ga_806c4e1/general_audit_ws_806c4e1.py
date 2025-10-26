# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWS806C4E1(models.Model):
    _name = "general_audit_ws_806c4e1"
    _description = (
        "Acceptance and Continuance of " "Client Relationships Analysis (806c4e1)"
    )
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_acceptance_continuance." "worksheet_type_806c4e1"
    )
    _checklist_model_name = "general_audit_ws_806c4e1.checklist"
    _item_model_name = "general_audit_ws_806c4e1.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_806c4e1.checklist",
        help="""Checklist lines for the Acceptance and Continuance of Client
Relationships analysis.""",
    )
    risk = fields.Selection(
        string="Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Aggregated risk level for the client acceptance/continuance decision.",
    )
    client_relationship = fields.Selection(
        string="Continue the Cient Relationship",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Decision whether to continue the client relationship based on the analysis.",
    )
    industry_id = fields.Many2one(
        related="general_audit_id.industry_id",
        help="Client's industry derived from the General Audit record.",
    )
    ownership_type_id = fields.Many2one(
        related="general_audit_id.ownership_type_id",
        help="Ownership type of the client derived from the General Audit record.",
    )

    @api.depends("general_audit_id", "general_audit_id.public_offering_ids")
    def _compute_public_offering(self):
        for record in self:
            record.public_offering = "No Public Offering"
            if (
                len(
                    record.general_audit_id.public_offering_ids.filtered(
                        lambda x: x.p2pk_go_public
                    )
                )
                >= 1
            ):
                record.public_offering = "Public Offering"

    public_offering = fields.Char(
        string="Public Offering",
        compute="_compute_public_offering",
        compute_sudo=True,
        store=True,
        help="""Computed status indicating whether the client has, or plans to have,
a public offering.""",
    )
    financial_accounting_standard_id = fields.Many2one(
        related="general_audit_id.financial_accounting_standard_id",
        help="""Applicable financial accounting standard for the engagement,
derived from the General Audit.""",
    )
    establishment_state = fields.Selection(
        string="Establishment Status",
        selection=[
            ("previous", "Established Previously"),
            ("new", "Newly Established"),
        ],
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Indicates whether the entity is previously established or newly established.",
    )
    financial_statement = fields.Selection(
        string="Prior Period Financial Statement",
        selection=[
            ("no_available", "Not Available"),
            ("available_no_audit", "Available but Unaudited"),
            ("available_audit", "Available and Audited"),
            ("not_relevant", "Not Relevant"),
        ],
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Availability status of prior period financial statements for the client.",
    )

    @api.depends("general_audit_id", "general_audit_id.num_of_consecutive_audit_firm")
    def _compute_engagemet(self):
        for record in self:
            record.engagemet = "Initial Engagement"
            if (record.general_audit_id.num_of_consecutive_audit_firm) >= 1:
                record.engagemet = "Recurring Engagement"

    engagemet = fields.Char(
        string="Engagement",
        compute="_compute_engagemet",
        compute_sudo=True,
        store=True,
        help="""Computed engagement type based on the number of consecutive audits
with the firm ('Initial Engagement' vs 'Recurring Engagement').""",
    )

    # LINK - 1 (PE.110.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_1_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_1_ids = obj.search(criteria).ids

    allowed_link_1_ids = fields.Many2many(
        string="Allowed Link 1",
        comodel_name="general_audit_ws_369c5a5",
        compute="_compute_allowed_link_1_ids",
        store=False,
        help="""Eligible PE.110.1 worksheets from the same audit
that can be linked.""",
    )

    link_1 = fields.Many2one(
        string="PE.110.1",
        comodel_name="general_audit_ws_369c5a5",
        ondelete="restrict",
        help="""Selected PE.110.1 worksheet used for cross-referencing
and risk derivation.""",
    )
    link_1_risk = fields.Selection(
        string="Risk (PE.110.1)",
        related="link_1.risk",
        store=True,
        help="Risk level propagated from the linked PE.110.1 worksheet.",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_1(self):
        self.link_1 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_369c5a5"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_1 = result.id

    # LINK - 2 (PE.110.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_2_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_2_ids = obj.search(criteria).ids

    allowed_link_2_ids = fields.Many2many(
        string="Allowed Link 2",
        comodel_name="general_audit_ws_f5e7049",
        compute="_compute_allowed_link_2_ids",
        store=False,
        help="""Eligible PE.110.2 worksheets from the same audit
that can be linked.""",
    )
    link_2 = fields.Many2one(
        string="PE.110.2",
        comodel_name="general_audit_ws_f5e7049",
        ondelete="restrict",
        help="""Selected PE.110.2 worksheet used for cross-referencing
and risk derivation.""",
    )
    link_2_risk = fields.Selection(
        string="Risk (PE.110.2)",
        related="link_2.risk",
        store=True,
        help="Risk level propagated from the linked PE.110.2 worksheet.",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_2(self):
        self.link_2 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_f5e7049"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_2 = result.id

    # LINK - 3 (PE.110.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_3_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_3_ids = obj.search(criteria).ids

    allowed_link_3_ids = fields.Many2many(
        string="Allowed Link 3",
        comodel_name="general_audit_ws_b9d8a5c",
        compute="_compute_allowed_link_3_ids",
        store=False,
        help="""Eligible PE.110.3 worksheets from the same audit
that can be linked.""",
    )
    link_3 = fields.Many2one(
        string="PE.110.3",
        comodel_name="general_audit_ws_b9d8a5c",
        ondelete="restrict",
        help="""Selected PE.110.3 worksheet used for cross-referencing
and risk derivation.""",
    )
    link_3_risk = fields.Selection(
        string="Risk (PE.110.3)",
        related="link_3.risk",
        store=True,
        help="Risk level propagated from the linked PE.110.3 worksheet.",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_3(self):
        self.link_3 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_b9d8a5c"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_3 = result.id

    # LINK - 4 (PE.110.4)
    @api.depends(
        "general_audit_id",
    )
    def _compute_allowed_link_4_ids(self):
        for record in self:
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            record.allowed_link_4_ids = obj.search(criteria).ids

    allowed_link_4_ids = fields.Many2many(
        string="Allowed Link 4",
        comodel_name="general_audit_ws_0427d28",
        compute="_compute_allowed_link_4_ids",
        store=False,
        help="""Eligible PE.110.4 worksheets from the same audit
that can be linked.""",
    )
    link_4 = fields.Many2one(
        string="PE.110.4",
        comodel_name="general_audit_ws_0427d28",
        ondelete="restrict",
        help="""Selected PE.110.4 worksheet used for cross-referencing
and risk derivation.""",
    )
    link_4_risk = fields.Selection(
        string="Risk (PE.110.4)",
        related="link_4.risk",
        store=True,
        help="Risk level propagated from the linked PE.110.4 worksheet.",
    )

    @api.onchange(
        "general_audit_id",
    )
    def onchange_link_4(self):
        self.link_4 = False
        if self.general_audit_id:
            obj = self.env["general_audit_ws_0427d28"]
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
            ]
            result = obj.search(criteria)
            if result:
                self.link_4 = result.id
