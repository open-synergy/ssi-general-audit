# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSae48e68(models.Model):
    """
    WS.050.1 — External Communication Schedule (ae48e68)

    Master schedule for documenting planned and actual **external
    communications** during the engagement.  As required by ISA 260 /
    SA 260 (Communication with Those Charged with Governance), ISA 265 /
    SA 265 (Communicating Deficiencies in Internal Control), and
    ISA 315 / SA 315, the auditor must plan and execute timely
    communication with:

    - **Management** (planning, execution, and reporting phases).
    - **Those Charged with Governance (TCWG)** (planning, execution, and
      reporting phases).
    - **Internal Audit (IA)** (planning, execution, and reporting phases).

    This worksheet captures the planned and actual dates for each
    communication phase alongside a general checklist confirming all
    required communication activities have been completed.

    **ISA / SA references:** ISA 260 / SA 260 — Communication with TCWG;
    ISA 265 / SA 265 — Communicating Deficiencies in Internal Control;
    ISA 315 / SA 315 — Identifying and Assessing the Risks of Material
    Misstatement
    """

    _name = "general_audit_ws_ae48e68"
    _description = "External Communication (ae48e68)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_external_communication." "worksheet_type_ae48e68"
    )
    _checklist_model_name = "general_audit_ws_ae48e68.checklist"
    _item_model_name = "general_audit_ws_ae48e68.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_ae48e68.checklist",
        help="All checklist line records associated with this worksheet.",
    )
    mgmt_communication_planning_date = fields.Date(
        string="Date of Management Communication Planning",
        help=(
            "Date when the communication planning with the " "Management was conducted."
        ),
    )
    mgmt_communication_date = fields.Date(
        string="Date of Management Communication",
        help=("Date when the communication with the Management was conducted."),
    )
    mgmt_communication_reporting_date = fields.Date(
        string="Date of Management Communication Reporting",
        help="Date when the communication reporting to the Management was conducted.",
    )
    tcwg_communication_planning_date = fields.Date(
        string="Date of TCWG Communication Planning",
        help="Date when the communication planning with the " "TCWG was conducted.",
    )
    tcwg_communication_date = fields.Date(
        string="Date of TCWG Communication",
        help="Date when the communication with the TCWG was conducted.",
    )
    tcwg_communication_reporting_date = fields.Date(
        string="Date of TCWG Communication Reporting",
        help="Date when the communication reporting to the TCWG was conducted.",
    )
    ia_communication_planning_date = fields.Date(
        string="Date of IA Communication Planning",
        help="Date when the communication planning with Internal Audit was conducted.",
    )
    ia_communication_date = fields.Date(
        string="Date of IA Communication",
        help="Date when the communication with Internal Audit was conducted.",
    )
    ia_communication_reporting_date = fields.Date(
        string="Date of IA Communication Reporting",
        help="Date when the communication reporting to Internal Audit was conducted.",
    )
