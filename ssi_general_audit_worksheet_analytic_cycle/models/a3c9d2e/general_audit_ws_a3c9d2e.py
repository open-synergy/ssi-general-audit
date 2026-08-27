# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import api, fields, models


class GeneralAuditWSA3C9D2E(models.Model):
    """WS: Analytical Procedures – Cycle (a3c9d2e) — SA 520.

    Documents the analytical procedures performed for one business cycle
    (``business_cycle_id``). Categories are added manually, one at a
    time ("Add Line"), from the master categories of the selected cycle
    (``general_audit_ws_a3c9d2e.item``); within each category the
    auditor records the specific procedures performed (also added
    manually, from that category's master items) together with their
    individual result.

    ``related_account_type_ids`` tags the Standard Accounts covered by
    this cycle as a whole (mirrors the single "Standard Account" field
    shown on the KKA template, next to "Siklus"). The worksheet's own
    ``conclusion_id`` (High/Moderate — see
    ``data/master/general_audit_worksheet_conclusion.xml``) is
    propagated to every matched ``general_audit.standard_detail`` (see
    :meth:`_inverse_to_standard_detail`); per-procedure results are
    working-paper documentation only and are not propagated.
    """

    _name = "general_audit_ws_a3c9d2e"
    _description = "Analytical Procedures – Cycle (a3c9d2e)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_analytic_cycle" ".worksheet_type_a3c9d2e"
    )
    _checklist_model_name = "general_audit_ws_a3c9d2e.checklist"
    _item_model_name = "general_audit_ws_a3c9d2e.item"
    _checklist_create_page = False

    business_cycle_id = fields.Many2one(
        string="Business Cycle",
        comodel_name="client_business_process",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Business cycle being analyzed in this worksheet.",
    )
    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_a3c9d2e.checklist",
        help=(
            "Analytical procedure categories for this cycle, added "
            "manually one at a time from the selected business cycle's "
            "master categories."
        ),
    )
    related_account_type_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_a3c9d2e_2_account_type",
        column1="worksheet_id",
        column2="type_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help="Standard accounts relevant to this cycle as a whole.",
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Details",
        comodel_name="general_audit.standard_detail",
        relation="rel_general_audit_ws_a3c9d2e_2_standard_detail",
        column1="worksheet_id",
        column2="standard_detail_id",
        compute="_compute_standard_detail_ids",
        store=True,
        compute_sudo=True,
        help=(
            "Standard details matched to the related standard accounts "
            "within this General Audit."
        ),
    )

    def _get_fields_required_before_confirm(self):
        """Require a business cycle, its Standard Accounts, and at least
        one populated category."""
        res = super()._get_fields_required_before_confirm()
        return res + ["business_cycle_id", "related_account_type_ids", "checklist_ids"]

    @api.depends("related_account_type_ids")
    def _compute_standard_detail_ids(self):
        """Match the tagged Standard Accounts to this engagement's details."""
        StandardDetail = self.env["general_audit.standard_detail"]
        for record in self:
            result = []
            if record.general_audit_id and record.related_account_type_ids:
                criteria = [
                    ("general_audit_id", "=", record.general_audit_id.id),
                    ("type_id", "in", record.related_account_type_ids.ids),
                ]
                result = StandardDetail.search(criteria).ids
            record.standard_detail_ids = result

    def _get_analytical_procedures_cycle_result(self):
        """Map ``conclusion_id`` to the High/Moderate result value.

        ``conclusion_id`` is generic master data
        (``general_audit_worksheet_conclusion``, scoped by ``type_id``);
        the High/Moderate records for this worksheet type are seeded by
        ``data/master/general_audit_worksheet_conclusion.xml`` and
        matched here by XML ID rather than by (translatable) name.
        """
        self.ensure_one()
        high = self.env.ref(
            "ssi_general_audit_worksheet_analytic_cycle."
            "general_audit_worksheet_conclusion_a3c9d2e_high",
            raise_if_not_found=False,
        )
        moderate = self.env.ref(
            "ssi_general_audit_worksheet_analytic_cycle."
            "general_audit_worksheet_conclusion_a3c9d2e_moderate",
            raise_if_not_found=False,
        )
        if high and self.conclusion_id.id == high.id:
            return "high"
        if moderate and self.conclusion_id.id == moderate.id:
            return "moderate"
        return False

    def _inverse_to_standard_detail(self):
        """Propagate the worksheet's cycle result to the matched standard details."""
        for record in self:
            result = record._get_analytical_procedures_cycle_result()
            if result and record.standard_detail_ids:
                record.standard_detail_ids.write(
                    {"analytical_procedures_cycle_result": result}
                )

    def write(self, vals):
        """Re-propagate the result whenever it or the account tags change."""
        res = super().write(vals)
        if {"conclusion_id", "related_account_type_ids"} & set(vals.keys()):
            self._inverse_to_standard_detail()
        return res
