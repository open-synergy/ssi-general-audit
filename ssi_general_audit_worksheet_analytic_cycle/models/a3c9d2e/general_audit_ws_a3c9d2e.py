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
    ``result`` (High/Moderate) is propagated to every matched
    ``general_audit.standard_detail`` (see
    :meth:`_inverse_to_standard_detail`), which recomputes each account
    from all non-cancelled worksheets covering it (``high`` outranks
    ``moderate``) and clears it when none remains. ``conclusion_id``/
    ``conclusion`` remain the mixin's generic
    required-before-confirm fields and are not used for this
    propagation. Per-procedure results
    (``checklist_ids.procedure_ids.result``) are working-paper
    documentation only and are not propagated.
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

    result = fields.Selection(
        string="Result",
        selection=[
            ("high", "High"),
            ("moderate", "Moderate"),
        ],
        help=(
            "High/Moderate result of the analytical procedures for "
            "this cycle. Determines the value propagated to the "
            "matched Standard Details' Analytical Procedures Cycle "
            "Result (see _inverse_to_standard_detail); independent "
            "of conclusion_id/conclusion, which remain the mixin's "
            "generic required-before-confirm fields."
        ),
    )
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
    checklist_conclusion_ids = fields.One2many(
        string="Conclusion",
        comodel_name="general_audit_ws_a3c9d2e.checklist",
        inverse_name="worksheet_id",
        help=(
            "Display alias of checklist_ids (same relation and data), "
            "used only by the Analytical Procedure Cycle Conclusion tab. "
            "Odoo deduplicates a field's sub-views when the same field is "
            "shown twice on one form with different tree/form layouts, so "
            "a separate field is needed here to give the Conclusion tab "
            "its own columns without affecting the Checklist tab."
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
        """Return this worksheet's own :attr:`result` for propagation.

        :return: ``"high"``, ``"moderate"``, or ``False`` when
            :attr:`result` is not set.
        :rtype: str or bool
        """
        self.ensure_one()
        if self.result == "high":
            return "high"
        if self.result == "moderate":
            return "moderate"
        return False

    def _get_live_standard_details(self):
        """Return the standard details currently covered by these sheets.

        Derived from a direct search on ``related_account_type_ids`` and
        ``general_audit_id`` rather than from the stored
        ``standard_detail_ids`` cache, which may lag behind a write.

        :return: ``general_audit.standard_detail`` recordset (sudo)
        """
        StandardDetail = self.env["general_audit.standard_detail"].sudo()
        result = StandardDetail
        for record in self.sudo():
            if record.general_audit_id and record.related_account_type_ids:
                result |= StandardDetail.search(
                    [
                        ("general_audit_id", "=", record.general_audit_id.id),
                        ("type_id", "in", record.related_account_type_ids.ids),
                    ]
                )
        return result

    def _inverse_to_standard_detail(self, standard_details=None):
        """Recompute the cycle result of every affected standard detail.

        For each standard detail (those covered by these worksheets plus
        ``standard_details``, typically the ones covered before a change)
        the value is re-derived from a live search of every non-cancelled
        worksheet of the same General Audit that tags its account and
        has a ``result``. ``high`` outranks ``moderate``; when no such
        worksheet remains the value is cleared (``False``).

        :param standard_details: extra ``general_audit.standard_detail``
            records to recompute, e.g. accounts that were just removed
            from ``related_account_type_ids``
        :return: nothing; writes ``analytical_procedures_cycle_result``
        """
        Worksheet = self.env["general_audit_ws_a3c9d2e"].sudo()
        details = self._get_live_standard_details()
        if standard_details:
            details |= standard_details.sudo()
        for detail in details.exists():
            worksheets = Worksheet.search(
                [
                    ("general_audit_id", "=", detail.general_audit_id.id),
                    ("related_account_type_ids", "in", detail.type_id.ids),
                    ("state", "!=", "cancel"),
                    ("result", "!=", False),
                ]
            )
            results = [w._get_analytical_procedures_cycle_result() for w in worksheets]
            if "high" in results:
                value = "high"
            elif "moderate" in results:
                value = "moderate"
            else:
                value = False
            if detail.analytical_procedures_cycle_result != value:
                detail.write({"analytical_procedures_cycle_result": value})

    @api.model_create_multi
    def create(self, vals_list):
        """Propagate the result of new worksheets carrying result/accounts.

        :param vals_list: list of values dicts for the new worksheets
        :return: the created worksheets
        """
        records = super().create(vals_list)
        if any({"result", "related_account_type_ids"} & set(v) for v in vals_list):
            records._inverse_to_standard_detail()
        return records

    def write(self, vals):
        """Re-propagate the result when it, the accounts or the state change.

        The standard details covered *before* the write are recomputed
        too, so an account removed from the worksheet (or whose worksheet
        was cancelled or emptied) loses a stale value.

        :param vals: values being written
        :return: result of the parent ``write``
        """
        triggers = {"result", "related_account_type_ids", "state", "general_audit_id"}
        propagate = bool(triggers & set(vals.keys()))
        before = self._get_live_standard_details() if propagate else None
        res = super().write(vals)
        if propagate:
            self._inverse_to_standard_detail(standard_details=before)
        return res

    def unlink(self):
        """Clear the cycle result of accounts only covered by these sheets.

        :return: result of the parent ``unlink``
        """
        before = self._get_live_standard_details()
        res = super().unlink()
        self.env["general_audit_ws_a3c9d2e"]._inverse_to_standard_detail(
            standard_details=before
        )
        return res
