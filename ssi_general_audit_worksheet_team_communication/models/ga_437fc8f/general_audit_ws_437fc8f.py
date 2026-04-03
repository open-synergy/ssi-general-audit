# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS437fc8f(models.Model):
    """Worksheet: Team Communication - Pre-Engagement (437fc8f).

    Documents the engagement team's communication during the pre-engagement
    and early planning phase of a general audit engagement, in accordance with
    ISQC 1 / SA 220 (Quality Control for Audit Engagements) and
    ISA 265 / SA 265 (Communicating Deficiencies in Internal Control).

    This worksheet captures the structured discussion between engagement team
    members on topics such as:
    - Engagement acceptance and continuance decisions (SA 220)
    - Team competencies, roles, and independence (ISQC 1)
    - Pre-engagement consultations with specialists or senior personnel
    - Planning dates for communication activities

    Checklist items are classified by ``communication_type``:
    - ``understanding``: engagement team understanding (pre-engagement matters)
    - ``consultation``: consultations conducted during or prior to the engagement

    Inherits from:
    - ``general_audit_worksheet_mixin``: standard audit worksheet lifecycle
      (state machine, sequence, audit link, approval)
    - ``mixin.checklist``: checklist item population from master item list
    """

    _name = "general_audit_ws_437fc8f"
    _description = "Team Communication Pre-Engagement (437fc8f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_team_communication." "worksheet_type_437fc8f"
    )
    _checklist_model_name = "general_audit_ws_437fc8f.checklist"
    _item_model_name = "general_audit_ws_437fc8f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_437fc8f.checklist",
        help=(
            "Collection of checklist items for this worksheet. "
            "Each checklist item represents a specific audit point "
            "that needs to be evaluated and documented."
        ),
    )
    communication_planning_date = fields.Date(
        string="Communication Planning Date",
        help=(
            "The date when the communication planning for the audit "
            "engagement was conducted."
        ),
    )
    communication_date = fields.Date(
        string="Communication Date",
        help="The date when the team communication took place.",
    )
    communication_reporting_date = fields.Date(
        string="Communication Reporting Date",
        help=(
            "The date when the communication reporting was completed " "and documented."
        ),
    )
