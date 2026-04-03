# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSC0E0EEC(models.Model):
    """Worksheet: Fraud Factor Analysis (c0e0eec).

    Documents the auditor's assessment of fraud risk indicators at the entity
    level, in accordance with ISA 240 / SA 240 — The Auditor's
    Responsibilities Relating to Fraud in an Audit of Financial Statements.

    ISA 240 requires auditors to identify and assess risks of material
    misstatement due to fraud. Fraud risks are categorized by the fraud
    triangle: incentives/pressures, opportunities, and attitudes/rationalizations.
    This worksheet operationalises this requirement through a structured
    checklist of fraud factor indicators drawn from master data.

    When populated (via ``action_populate``), the worksheet creates detail lines
    for all active fraud factor indicators (``general_audit_fraud_factor_indicator``).
    For each indicator, the auditor documents observations across three
    information sources:
    - ``tcgw``: Those Charged With Governance observations
    - ``management``: Management attitudes and behaviours
    - ``other``: Other corroborative information

    Results feed into the overall risk of material misstatement assessment
    and the design of fraud-responsive audit procedures.

    Inherits from ``general_audit_worksheet_mixin``.
    """

    _name = "general_audit_ws_c0e0eec"
    _description = "Fraud Factor Analysis (c0e0eec)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_c0e0eec"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_c0e0eec.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Fraud indicator assessment lines for this worksheet. "
            "Re-loaded from master indicators when the worksheet is opened."
        ),
    )

    def action_populate(self):
        for record in self:
            record._populate()

    def _populate(self):
        self.ensure_one()
        Detail = self.env["general_audit_ws_c0e0eec.detail"]
        Indicator = self.env["general_audit_fraud_factor_indicator"]

        indicator_ids = Indicator.search([])
        mapping = {chk.indicator_id.id: chk for chk in self.detail_ids}

        for indicator in indicator_ids:
            if indicator.id not in mapping:
                Detail.create(
                    {
                        "worksheet_id": self.id,
                        "indicator_id": indicator.id,
                    }
                )

        for chk in self.detail_ids:
            if chk.indicator_id.id not in indicator_ids.ids:
                chk.unlink()
