# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSc0d0898(models.Model):
    """Worksheet: Going Concern Analysis — Preliminary (c0d0898) — RA.150.8.

    Documents the auditor's preliminary assessment of going concern indicators
    at the entity level during the planning/understanding phase of the audit,
    in accordance with:
    - ISA 315 (Revised) / SA 315 — Understanding the entity
    - ISA 570 (Revised) / SA 570 — Going Concern

    This is a preliminary assessment (performed at the understanding stage)
    that precedes the more detailed going concern analysis performed during
    execution (see ``general_audit_ws_fbf57ee`` in the specific procedures
    module). It flags early indicators of financial distress or uncertainty
    about the entity's ability to continue as a going concern.

    When the worksheet is opened, it is automatically populated with all
    going concern indicators from the master list (``general_audit_going_concern``).
    For each indicator, the auditor assesses:
    - Whether the indicator exists at the entity (``going_concern_exist``)
    - The potential impact on the financial report (``consideration``)

    Inherits from ``general_audit_worksheet_mixin``.
    """

    _name = "general_audit_ws_c0d0898"
    _description = "Going concern analysis (c0d0898)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_c0d0898"
    )

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_c0d0898.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Going concern assessment lines for this worksheet. "
            "Re-loaded from master list when the worksheet is opened."
        ),
    )

    @ssi_decorator.post_open_action()
    def _01_reload_item(self):
        self.ensure_one()
        self.detail_ids.unlink()
        GoingConcern = self.env["general_audit_going_concern"]
        Detail = self.env["general_audit_ws_c0d0898.detail"]
        for gc in GoingConcern.search([]):
            data = {
                "going_concern_id": gc.id,
                "worksheet_id": self.id,
            }
            Detail.create(data)
