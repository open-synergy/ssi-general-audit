# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSf87b2e1(models.Model):
    _name = "general_audit_ws_f87b2e1"
    _description = "Understanding of The Entity and it's Environment (f87b2e1)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_f87b2e1"
    )

    def action_reload_links(self):
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        self.ensure_one()
        self._compute_link_1_id()
        self._compute_link_2_id()
        self._compute_link_3_id()
        self._compute_link_4_id()
        # self._compute_link_5_id()
        self._compute_link_6_id()
        self._compute_link_7_id()
        self._compute_link_8_id()

    # General Information and Legal Aspec
    # LINK - 1 ddf034c (RA.150.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ddf034c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.id
            record.link_1_id = result

    link_1_id = fields.Many2one(
        string="RA.150.1",
        comodel_name="general_audit_ws_ddf034c",
        compute_sudo=True,
        compute="_compute_link_1_id",
        store=True,
        help=(
            "Link to worksheet RA.150.1 (General Information and Legal Aspect) for this "
            "General Audit. Automatically computed and stored for quick access."
        ),
    )
    link_1_state = fields.Selection(
        string="State (RA.150.1)",
        related="link_1_id.state",
        help=(
            "Workflow state of the linked RA.150.1 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_1_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.1)",
        related="link_1_id.conclusion_id",
        help=(
            "Conclusion selected on the RA.150.1 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Structure Organization and Responsibilities
    # LINK - 2 e78a3c6 (RA.150.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e78a3c6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.id
            record.link_2_id = result

    link_2_id = fields.Many2one(
        string="RA.150.2",
        comodel_name="general_audit_ws_e78a3c6",
        compute_sudo=True,
        compute="_compute_link_2_id",
        store=True,
        help=(
            "Link to worksheet RA.150.2 (Structure Organization and Responsibilities) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_2_state = fields.Selection(
        string="State (RA.150.2)",
        related="link_2_id.state",
        help=(
            "Workflow state of the linked RA.150.2 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_2_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.2)",
        related="link_2_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.2 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Main Business Activity Process
    # LINK - 3 ae11f7e (RA.150.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_3_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae11f7e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_3_ids = obj.search(criteria)
            if link_3_ids:
                result = link_3_ids.id
            record.link_3_id = result

    link_3_id = fields.Many2one(
        string="RA.150.3",
        comodel_name="general_audit_ws_ae11f7e",
        compute_sudo=True,
        compute="_compute_link_3_id",
        store=True,
        help=(
            "Link to worksheet RA.150.3 (Main Business Activity Process) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_3_state = fields.Selection(
        string="State (RA.150.3)",
        related="link_3_id.state",
        help=(
            "Workflow state of the linked RA.150.3 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_3_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.3)",
        related="link_3_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.3 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Understanding of Relevant Regulations
    # LINK - 4 a13a30e (RA.150.4)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_4_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a13a30e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_4_ids = obj.search(criteria)
            if link_4_ids:
                result = link_4_ids.id
            record.link_4_id = result

    link_4_id = fields.Many2one(
        string="RA.150.4",
        comodel_name="general_audit_ws_a13a30e",
        compute_sudo=True,
        compute="_compute_link_4_id",
        store=True,
        help=(
            "Link to worksheet RA.150.4 (Understanding of Relevant Regulations) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_4_state = fields.Selection(
        string="State (RA.150.4)",
        related="link_4_id.state",
        help=(
            "Workflow state of the linked RA.150.4 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_4_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.4)",
        related="link_4_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.4 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Understanding of the business environment
    # LINK - 5 bdcdfc5 (RA.150.5)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_5_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bdcdfc5"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_5_ids = obj.search(criteria)
            if link_5_ids:
                result = link_5_ids.ids
            record.link_5_ids = result

    link_5_ids = fields.Many2many(
        string="RA.150.5",
        comodel_name="general_audit_ws_bdcdfc5",
        compute_sudo=True,
        compute="_compute_link_5_ids",
        store=True,
        help=(
            "Collection of all RA.150.5 (Understanding of the Business Environment) "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Going Concern Analysis
    # LINK - 6 c0d0898 (RA.150.6)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_6_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c0d0898"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_6_ids = obj.search(criteria)
            if link_6_ids:
                result = link_6_ids.id
            record.link_6_id = result

    link_6_id = fields.Many2one(
        string="RA.150.6",
        comodel_name="general_audit_ws_c0d0898",
        compute_sudo=True,
        compute="_compute_link_6_id",
        store=True,
        help=(
            "Link to worksheet RA.150.6 (Going Concern Analysis) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_6_state = fields.Selection(
        string="State (RA.150.6)",
        related="link_6_id.state",
        help=(
            "Workflow state of the linked RA.150.6 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_6_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.6)",
        related="link_6_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.6 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Understanding of Preparation of Financial Statements
    # LINK - 7 f6a227 (RA.150.7)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_7_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f6a227"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_7_ids = obj.search(criteria)
            if link_7_ids:
                result = link_7_ids.id
            record.link_7_id = result

    link_7_id = fields.Many2one(
        string="RA.150.7",
        comodel_name="general_audit_ws_f6a227",
        compute_sudo=True,
        compute="_compute_link_7_id",
        store=True,
        help=(
            "Link to worksheet RA.150.7 (Understanding of Preparation of Financial "
            "Statements) for this General Audit. Automatically computed and stored."
        ),
    )
    link_7_state = fields.Selection(
        string="State (RA.150.7)",
        related="link_7_id.state",
        help=(
            "Workflow state of the linked RA.150.7 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_7_conclusion_id = fields.Many2one(
        string="Conclusion (RA.150.7)",
        related="link_7_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.7 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Fraud Factor Analysis
    # LINK - 8 c0e0eec (RA.150.8)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_8_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c0e0eec"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_8_ids = obj.search(criteria)
            if link_8_ids:
                result = link_8_ids.id
            record.link_8_id = result

    link_8_id = fields.Many2one(
        string="RA.150.8",
        comodel_name="general_audit_ws_c0e0eec",
        compute_sudo=True,
        compute="_compute_link_8_id",
        store=True,
        help=(
            "Link to worksheet RA.150.8 (Fraud Factor Analysis) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_8_state = fields.Selection(
        related="link_8_id.state",
        help=(
            "Workflow state of the linked RA.150.8 worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_8_conclusion_id = fields.Many2one(
        related="link_8_id.conclusion_id",
        help=(
            "Conclusion from the RA.150.8 worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
