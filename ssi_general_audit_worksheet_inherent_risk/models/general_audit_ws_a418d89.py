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
        """
        self.ensure_one()
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
