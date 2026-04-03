# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSb59b886(models.Model):
    """Worksheet — Control Risk at Entity Level (b59b886).

    Evaluates the entity-level control environment by assessing general
    controls (``general_control_ids``) and IT general controls (``it_control_ids``)
    drawn from confirmed evaluation worksheets (d3d2719 and f63f569 respectively).

    The ``action_populate`` method auto-imports the detailed evaluation results
    from those upstream worksheets into this entity-level view.  The auditor
    then records whether any control deficiency or significant deficiency has
    been identified, and provides an overall conclusion.

    Feeds into the Control Risk Summary worksheet (a58e29c) and, where
    deficiencies are identified, into the Control Deficiencies worksheet
    (WR.110.2 / d33420f).

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 315/SA 315 (Identifying and Assessing Risks);
    ISA 265/SA 265 (Communicating Deficiencies in Internal Control).
    """

    _name = "general_audit_ws_b59b886"
    _description = "Control Risk - Entity Level (b59b886)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_control_risk." "worksheet_type_b59b886"

    general_control_ids = fields.One2many(
        string="Evaluation of Control Understanding",
        comodel_name="general_audit_ws_b59b886.general_control",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    it_control_ids = fields.One2many(
        string="Evaluation of Information Technology Controls",
        comodel_name="general_audit_ws_b59b886.it_control",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )
    control_deficiency_identified = fields.Selection(
        string="Control Deficiency",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )

    significant_deficiency_identified = fields.Selection(
        string="Significant Deficiency",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
    )

    def action_populate(self):
        for record in self.sudo():
            record._populate(
                "general_audit_ws_b59b886.general_control",
                "general_control_ids",
                "general_audit_ws_d3d2719.detail",
            )
            record._populate(
                "general_audit_ws_b59b886.it_control",
                "it_control_ids",
                "general_audit_ws_f63f569.detail",
            )

    def _populate(self, detail_obj, detail_field, ws_obj):
        Detail = self.env[detail_obj]
        Worksheet = self.env[ws_obj]

        for record in self:
            worksheets = Worksheet.search(
                [
                    ("worksheet_id.general_audit_id", "=", record.general_audit_id.id),
                ]
            )
            mapping = {chk.detail_id.id: chk for chk in record[detail_field]}

            for ws in worksheets:
                if ws.id not in mapping:
                    Detail.create(
                        {
                            "worksheet_id": record.id,
                            "detail_id": ws.id,
                        }
                    )

            worksheet_ids = set(worksheets.ids)
            for chk in record[detail_field]:
                if chk.detail_id.id not in worksheet_ids:
                    chk.unlink()

    @ssi_decorator.post_open_action()
    def _10_populate_data(self):
        self.ensure_one()
        self.action_populate()
