# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSd66d87a(models.Model):
    """
    WS: Account / Assertion Level ROMM (d66d87a) — ISA 315 / SA 315.

    Captures the **risk of material misstatement at the account and assertion
    level** for each standard detail in the General Audit engagement.
    This is the primary working paper where the auditor records:

    * **Inherent risk** — the susceptibility of an assertion to a material
      misstatement before considering controls.
    * **Control risk** — the risk that a material misstatement will not be
      prevented or detected by internal controls.
    * **Overall ROMM** — combined assessment of inherent and control risk.
    * **Fraud impact** — whether fraud risk factors affect the account.
    * **Planned responses** — which audit procedures are planned to address
      the risk: Analytical Procedures, Tests of Controls (ToC), Tests of
      Detail (ToD), or Interim procedures.

    Use ``action_load_detail`` to auto-populate lines from all standard
    details in the system.  The results flow into the Financial Level ROMM
    worksheet and drive the selection of audit procedures in the Lead
    Schedule (Key Audit Procedures worksheet).
    """

    _name = "general_audit_ws_d66d87a"
    _description = "Account Level ROMM (d66d87a)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_d66d87a"

    romm_scoring_config_id = fields.Many2one(
        string="Risk Configuration",
        comodel_name="general_audit_romm_scoring_config",
        default=lambda self: self.env[
            "general_audit_romm_scoring_config"
        ]._get_config(),
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Risk Configuration pinned to this worksheet at creation time "
            "(defaults to the one active in Settings then, left blank if "
            "none exists yet). All ROMM computations on this worksheet's "
            "lines use this record, not whatever is currently active in "
            "Settings - so historical worksheets stay reproducible even if "
            "the active Risk Configuration is changed or replaced later."
        ),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_d66d87a.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Lines generated for each standard detail to capture assertion-level ROMM "
            "and planned responses at the account level."
        ),
    )

    def action_load_detail(self):
        """
        Populate ``detail_ids`` from the standard details of this
        worksheet's engagement.

        Triggers :meth:`_load_detail` (wrapped in ``sudo()``) for every
        record in the current recordset.
        """
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        """
        Rebuild ``detail_ids`` from ``general_audit.standard_detail``.

        Existing lines are removed, then one line is created for each
        standard detail that belongs to this worksheet's
        ``general_audit_id`` — the search is scoped so that standard
        details from other audit engagements are never loaded here.

        :meth:`_resync_inherent_risk` runs first so that ``action_load_detail``
        also repairs any standard detail whose ``inherent_risk`` was never
        propagated from the Account Level Inherent Risk worksheet — the
        new lines created below read ``standard_detail_id.inherent_risk``
        (via the related/stored ``inherent_risk`` field on the detail
        model) at creation time, so they must see the corrected value.
        """
        self.ensure_one()
        self._resync_inherent_risk()
        self.detail_ids.unlink()
        StandardDetail = self.env["general_audit.standard_detail"]
        Detail = self.env["general_audit_ws_d66d87a.detail"]
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
        ]
        for standard_detail in StandardDetail.search(criteria):
            data = {
                "worksheet_id": self.id,
                "standard_detail_id": standard_detail.id,
            }
            Detail.create(data)

    def _resync_inherent_risk(self):
        """
        Re-propagate Inherent Risk from the Account Level Inherent Risk
        worksheet(s) (``general_audit_ws_a418d89``) onto
        ``general_audit.standard_detail`` for this worksheet's engagement.

        ``general_audit_ws_a418d89.detail.inherent_risk`` is a stored
        compute field that writes itself back to
        ``standard_detail_id.inherent_risk`` via ``_inverse_to_standard_detail``
        whenever the compute runs. If that propagation never fired for a
        line (e.g. it was created/updated outside the normal form/compute
        flow), the standard detail — and therefore this worksheet's
        related ``inherent_risk`` mirror — is left blank even though the
        Inherent Risk worksheet itself already holds the assessed value.
        Re-running the inverse here, scoped to this engagement, lets users
        fix that gap simply by clicking "Load Detail" again.
        """
        inherent_risk_worksheets = self.env["general_audit_ws_a418d89"].search(
            [("general_audit_id", "=", self.general_audit_id.id)]
        )
        inherent_risk_worksheets.mapped("detail_ids")._inverse_to_standard_detail()
