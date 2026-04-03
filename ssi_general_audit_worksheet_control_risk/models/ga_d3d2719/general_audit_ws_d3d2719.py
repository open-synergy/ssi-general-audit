# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSD3D2719(models.Model):
    """Worksheet — General Control Evaluation (d3d2719).

    Evaluates the design and operating effectiveness of entity-level **general
    (non-IT) controls** using a pre-configured control set (``set_id``).
    When ``action_load_detail`` is called, detail lines are generated
    automatically for every control in the set, and indicator lines are
    generated for each control's indicators.

    The auditor assigns a response (option from the control's ``option_set``)
    to each indicator.  The aggregated result feeds into the entity-level
    Control Risk worksheet (b59b886) via the populate mechanism.

    Typical controls covered: tone at the top, organisational structure,
    segregation of duties, authorisation policies, physical safeguards.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks).
    """

    _name = "general_audit_ws_d3d2719"
    _description = "General Control Evaluation (d3d2719)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_d3d2719"

    set_id = fields.Many2one(
        string="General Control Set",
        comodel_name="general_audit_general_control_set",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "General control set providing the controls and indicators to be "
            "evaluated."
        ),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_d3d2719.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Generated detail lines for each control in the selected set.",
    )
    indicator_ids = fields.One2many(
        string="Indicators",
        comodel_name="general_audit_ws_d3d2719.indicator",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Generated indicator lines for controls/indicators in the selected " "set."
        ),
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.detail_ids.unlink()
        Detail = self.env["general_audit_ws_d3d2719.detail"]
        Indicator = self.env["general_audit_ws_d3d2719.indicator"]
        general_control_set = self.set_id
        for control in general_control_set.general_control_ids:
            data = {
                "worksheet_id": self.id,
                "control_id": control.id,
            }
            detail = Detail.create(data)
            for indicator in general_control_set.general_control_indicator_ids.filtered(
                lambda r: r.control_id.id == control.id
            ):
                data = {
                    "detail_id": detail.id,
                    "indicator_id": indicator.id,
                }
                Indicator.create(data)
