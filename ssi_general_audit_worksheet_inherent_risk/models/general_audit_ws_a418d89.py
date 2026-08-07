# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSA418D89(models.Model):
    """
    WS.060.2 — Account Level Inherent Risk (a418d89)

    Documents the **account-level inherent risk assessment** for each
    standard detail (account / disclosure area) of the engagement, as
    required by ISA 315 / SA 315.  For each account the auditor assesses:

    - Inherent risk factors *without* direct impact — contextual factors
      that inform but do not automatically elevate the risk level.
    - Inherent risk factors *with* direct impact — factors whose
      presence directly raises the assessed risk.
    - **Likelihood of risk occurring** (low / high).
    - **Magnitude / impact of risk** (low / high).

    The resulting ``inherent_risk`` (low / medium / high) and
    ``significant_risk`` flag are computed from the likelihood and
    impact assessments, then written back to the linked
    ``general_audit.standard_detail`` record so that they are available
    to downstream worksheets (e.g. WS.060.3, WS.070 control risk,
    WS.080 materiality).

    Action ``action_load_detail`` populates one detail line per standard
    detail of the engagement.

    **ISA / SA references:** ISA 315 / SA 315 — Identifying and Assessing
    the Risks of Material Misstatement through Understanding the Entity
    and Its Environment
    """

    _name = "general_audit_ws_a418d89"
    _description = "Account Level Inherent Risk (a418d89)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_inherent_risk." "worksheet_type_a418d89"

    # risk_material_missstatement = fields.Selection(
    #     string="Risk Material Misstatement",
    #     selection=[
    #         ("low", "Low"),
    #         ("medium", "Medium"),
    #         ("high", "High"),
    #     ],
    #     readonly=True,
    #     required=False,
    #     states={
    #         "open": [
    #             ("readonly", False),
    #         ],
    #     },
    # )
    # auditor_respons = fields.Text(
    #     string="Auditor Respons",
    #     readonly=True,
    #     states={
    #         "open": [
    #             ("readonly", False),
    #         ],
    #     },
    # )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_a418d89.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Detail lines generated per standard detail of the engagement."
            "Used to assess inherent and significant risk at the account level; "
            "editable when the worksheet is Open."
        ),
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        """
        Reconcile ``detail_ids`` with ``general_audit_id.standard_detail_ids``.

        Only creates lines for standard details that don't have one yet
        and only unlinks lines whose standard detail is no longer part of
        the engagement. Existing (still-matching) lines are left
        untouched so that the auditor's risk assessment inputs
        (``inherent_risk_factor_*_ids``, ``likelihood_risk_occuring``,
        ``impact_of_risk``, ``other_significant_risk_factor``, ``note``)
        survive repeated clicks of "Load Detail" -- these fields have no
        other storage location, so wiping the line would destroy the
        data permanently (unlike e.g. ``general_audit_ws_d66d87a``, whose
        mirrored fields are recoverable from ``standard_detail_id``).

        :meth:`_resync_fraud_risk` runs first so that ``action_load_detail``
        also repairs any standard detail whose ``fraud_impacted`` was never
        recomputed after the account stopped matching the Fraud Factor
        Analysis worksheet -- since existing lines are otherwise never
        revisited by this method.
        """
        self.ensure_one()
        self._resync_fraud_risk()
        Detail = self.env["general_audit_ws_a418d89.detail"]

        all_standard_details = self.general_audit_id.standard_detail_ids
        existing_standard_details = self.detail_ids.mapped("standard_detail_id")

        standard_details_to_add = all_standard_details - existing_standard_details
        standard_details_to_remove = existing_standard_details - all_standard_details

        for standard_detail in standard_details_to_add:
            Detail.create(
                {
                    "worksheet_id": self.id,
                    "standard_detail_id": standard_detail.id,
                }
            )

        details_to_remove = self.detail_ids.filtered(
            lambda d: d.standard_detail_id in standard_details_to_remove
        )
        if details_to_remove:
            details_to_remove.unlink()

    def _resync_fraud_risk(self):
        """
        Repair the Fraud Factor Analysis -> standard detail propagation
        chain for this worksheet's engagement, so ``fraud_risk`` (related+
        stored from ``standard_detail_id.fraud_impacted``) reflects reality
        again before (re)loading detail lines.

        Two stored compute fields sit on this chain:
        ``general_audit_ws_c0e0eec.detail.standard_detail_ids`` (Many2many,
        depends on ``related_account_type_ids``) and
        ``general_audit.standard_detail.fraud_impacted`` (Boolean, depends
        on the reverse ``c0e0eec_detail_ids``). Both were confirmed (via
        direct testing against production data, ticket HT/26/000630 revisi
        07 Agustus 2026) to get stuck at their old value whenever the
        freshly computed value becomes *empty*: a genuine ``write()`` on
        ``related_account_type_ids`` clearing it to ``[]`` leaves the
        previously-linked ``standard_detail_ids`` untouched, even though
        the same field correctly picks up an *added* link. Odoo's
        automatic recompute of a stored-compute field simply does not
        reliably persist an emptied result.

        Calling the private ``_compute_*`` methods directly does not
        work around this either: ``Field.__set__`` only routes a plain
        attribute assignment on a store-without-inverse field through the
        real ``write()`` path when the record is "protected" (i.e.
        genuinely running inside Odoo's own ``env.protecting()`` recompute
        cycle) -- invoked directly like this, outside that cycle, the
        assignment is silently dropped and nothing is persisted.

        The only path proven to reliably persist a change is an explicit
        ``record.write({...})`` with a freshly re-derived value (the same
        technique already used by ``_inverse_to_standard_detail`` on this
        worksheet's own detail model) -- so that is what both layers use
        below, each re-derived from a live search rather than from
        (possibly still-stale) cached relation fields.
        """
        general_audit = self.general_audit_id
        StandardDetail = self.env["general_audit.standard_detail"]
        FraudDetail = self.env["general_audit_ws_c0e0eec.detail"]

        fraud_worksheets = self.env["general_audit_ws_c0e0eec"].search(
            [("general_audit_id", "=", general_audit.id)]
        )
        for detail in fraud_worksheets.mapped("detail_ids"):
            criteria = [
                ("general_audit_id", "=", general_audit.id),
                ("type_id", "in", detail.related_account_type_ids.ids),
            ]
            ids = StandardDetail.search(criteria).ids
            if set(ids) != set(detail.standard_detail_ids.ids):
                detail.write({"standard_detail_ids": [(6, 0, ids)]})

        for standard_detail in general_audit.standard_detail_ids:
            impacted = bool(
                FraudDetail.search_count(
                    [("standard_detail_ids", "=", standard_detail.id)]
                )
            )
            if standard_detail.fraud_impacted != impacted:
                standard_detail.write({"fraud_impacted": impacted})
