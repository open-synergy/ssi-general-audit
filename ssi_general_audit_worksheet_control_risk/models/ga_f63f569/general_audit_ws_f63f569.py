# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSF63F569(models.Model):
    """Worksheet — IT Control Evaluation (f63f569).

    Evaluates the design and operating effectiveness of **IT General Controls
    (ITGC)** using a pre-configured IT control set (``set_id``).
    When ``action_load_detail`` is called, detail and indicator lines are
    generated for each IT control and its indicators in the selected set.

    Typical ITGCs covered: logical access controls, change management, IT
    operations and availability, data backup and recovery.

    Results are aggregated into the entity-level Control Risk worksheet
    (b59b886) via the populate mechanism.  Significant ITGC deficiencies
    are escalated to the Control Deficiencies worksheet (WR.110.2).

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks);
    ISA 265/SA 265 (Communicating Deficiencies in Internal Control).
    """

    _name = "general_audit_ws_f63f569"
    _description = "IT Control Evaluation (f63f569)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_f63f569"

    set_id = fields.Many2one(
        string="IT Control Set",
        comodel_name="general_audit_it_control_set",
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "IT control set providing the controls and indicators to be " "evaluated."
        ),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f63f569.detail",
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
        comodel_name="general_audit_ws_f63f569.indicator",
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
        """Synchronise the control lines with the selected control set.

        Triggers :meth:`_load_detail` (wrapped in ``sudo()``) for every
        record in the current recordset.

        :return: nothing; adds and removes control and indicator lines
        """
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        """Synchronise ``detail_ids`` with the selected control set.

        Control lines are matched on ``control_id`` and indicator lines
        on ``indicator_id``. Missing lines are created, lines no longer
        in the set are removed and all others are left untouched, so the
        result and explanation entered by the auditor are never lost.
        An empty set removes every line.

        :return: nothing; adds and removes control and indicator lines
        """
        self.ensure_one()
        Detail = self.env["general_audit_ws_f63f569.detail"]
        Indicator = self.env["general_audit_ws_f63f569.indicator"]
        control_set = self.set_id
        wanted_controls = control_set.it_control_ids
        obsolete = self.detail_ids.filtered(
            lambda line: line.control_id not in wanted_controls
        )
        obsolete.unlink()
        kept = self.detail_ids - obsolete
        details = {line.control_id: line for line in kept}
        for control in wanted_controls:
            detail = details.get(control)
            if not detail:
                detail = Detail.create(
                    {
                        "worksheet_id": self.id,
                        "control_id": control.id,
                    }
                )
            wanted_indicators = control_set.it_control_indicator_ids.filtered(
                lambda r, control=control: r.control_id.id == control.id
            )
            stale = detail.indicator_ids.filtered(
                lambda line: line.indicator_id not in wanted_indicators
            )
            stale.unlink()
            present = (detail.indicator_ids - stale).mapped("indicator_id")
            for indicator in wanted_indicators - present:
                Indicator.create(
                    {
                        "detail_id": detail.id,
                        "indicator_id": indicator.id,
                    }
                )
