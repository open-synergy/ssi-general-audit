# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class GeneralAuditWSa58e29c(models.Model):
    """Worksheet — Control Risk Summary (a58e29c).

    Consolidates the results of all control-risk worksheets for a given general
    audit engagement onto a single view to support the auditor's final
    control-risk conclusion:

    * ``link_1_id``  — links to the Control Risk – Entity Level worksheet (b59b886),
      reflecting the entity-wide control environment assessment.
    * ``link_2_ids`` — links to all Business Cycle Internal Control worksheets
      (eabdaad) in the same engagement, one per in-scope business cycle.
    * ``link_3_id``  — links to the Key Audit Procedures worksheet (lead schedule)
      to provide traceability between the control-risk conclusion and the
      planned audit response.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks);
    ISA 330/SA 330 (Auditor's Responses to Assessed Risks).
    """

    _name = "general_audit_ws_a58e29c"
    _description = "Control Risk (a58e29c)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_a58e29c"

    def action_reload_links(self):
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        self.ensure_one()
        self._compute_link_1_id()
        self._compute_link_2_ids()
        self._compute_link_3_id()

    # Control Risk - Entity Level
    # LINK - 1 b59b886 (RA.220.1)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b59b886"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.id
            record.link_1_id = result

    link_1_id = fields.Many2one(
        string="RA.220.1",
        comodel_name="general_audit_ws_b59b886",
        compute_sudo=True,
        compute="_compute_link_1_id",
        store=True,
        help=(
            "Link to worksheet 'Control Risk - Entity Level' for this "
            "General Audit. Automatically computed and stored for quick access."
        ),
    )
    link_1_state = fields.Selection(
        string="State (RA.220.1)",
        related="link_1_id.state",
        help=(
            "Workflow state of the linked worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_1_conclusion_id = fields.Many2one(
        string="Conclusion (RA.220.1)",
        related="link_1_id.conclusion_id",
        help=(
            "Conclusion selected on the worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_1_conclusion = fields.Text(
        string="Conclusion",
        related="link_1_id.conclusion",
        help=("Conclusion on the worksheet. " "Read-only, mirrors the linked record."),
    )

    # Control Risk - Cycle Level
    # LINK - 2 eabdaad (RA.220.2)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_ids(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_eabdaad"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.ids
            record.link_2_ids = result

    link_2_ids = fields.Many2many(
        string="RA.220.2",
        comodel_name="general_audit_ws_eabdaad",
        compute_sudo=True,
        compute="_compute_link_2_ids",
        store=True,
        help=(
            "Collection of all 'Control Risk - Cycle Level' "
            "worksheets linked to this General Audit. Automatically computed; use it to "
            "navigate to each detailed worksheet."
        ),
    )

    # Significant Account
    # LINK - 3 ba9b2f0 (RA.220.3)
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_3_id(self):
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ba9b2f0"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
            ]
            link_3_ids = obj.search(criteria)
            if link_3_ids:
                result = link_3_ids.id
            record.link_3_id = result

    link_3_id = fields.Many2one(
        string="RA.220.3",
        comodel_name="general_audit_ws_ba9b2f0",
        compute_sudo=True,
        compute="_compute_link_3_id",
        store=True,
        help=(
            "Link to worksheet 'Significant Account' for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_3_state = fields.Selection(
        string="State (RA.220.3)",
        related="link_3_id.state",
        help=(
            "Workflow state of the linked worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_3_conclusion_id = fields.Many2one(
        string="Conclusion (RA.220.3)",
        related="link_3_id.conclusion_id",
        help=(
            "Conclusion from the worksheet. " "Read-only, mirrors the linked record."
        ),
    )
    link_3_conclusion = fields.Text(
        string="Conclusion",
        related="link_3_id.conclusion",
        help=("Conclusion on the worksheet. " "Read-only, mirrors the linked record."),
    )

    def _get_fields_required_before_confirm(self):
        _super = super(GeneralAuditWSa58e29c, self)
        res = _super._get_fields_required_before_confirm()
        res += ["link_1_id", "link_2_ids", "link_3_id"]
        return res

    def _get_custom_field_labels(self):
        return {
            "link_1_id": _("Control Risk - Entity Level"),
            "link_2_ids": _("Control Risk - Cycle Level"),
            "link_3_id": _("Significant Account"),
        }
