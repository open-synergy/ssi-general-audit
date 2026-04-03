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
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        self.detail_ids.unlink()
        StandardDetail = self.env["general_audit.standard_detail"]
        Detail = self.env["general_audit_ws_d66d87a.detail"]
        for standard_detail in StandardDetail.search([]):
            data = {
                "worksheet_id": self.id,
                "standard_detail_id": standard_detail.id,
            }
            Detail.create(data)
