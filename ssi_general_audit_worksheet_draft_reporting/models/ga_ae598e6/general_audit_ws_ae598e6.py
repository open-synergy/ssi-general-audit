# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSae598e6(models.Model):
    """Worksheet — Management Letter (ae598e6).

    Compiles the formal written communication to management (and/or TCWG)
    of findings and control deficiencies identified during the audit.  Content
    is auto-populated via ``action_populate`` from items marked as *escalated*
    in the Audit Result Discussion worksheet (WR.110.4 / bc3e272).

    Two categories of items are tracked:
    * ``influence_ids`` — findings that influence the audit opinion
      (from bc3e272.influence, linked back to WR.110.1 / a0319a2)
    * ``control_ids`` — control deficiencies
      (from bc3e272.control, linked back to WR.110.2 / d33420f)

    Under ISA 265 / SA 265, a management letter is the primary vehicle for
    communicating significant control deficiencies and material weaknesses
    to TCWG and management.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 260/SA 260 (Communication with TCWG);
    ISA 265/SA 265 (Communicating Deficiencies in Internal Control).
    """

    _name = "general_audit_ws_ae598e6"
    _description = "Management Letter (ae598e6)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_ae598e6"
    )

    influence_ids = fields.One2many(
        string="Findings That Influence Opinion",
        comodel_name="general_audit_ws_ae598e6.influence",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Lines referencing findings that may influence the audit opinion; "
            "populated from worksheet bc3e272."
        ),
    )
    control_ids = fields.One2many(
        string="Control Deficiencies",
        comodel_name="general_audit_ws_ae598e6.control",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Lines referencing identified control deficiencies; "
            "populated from worksheet bc3e272."
        ),
    )

    def action_populate(self):
        for record in self.sudo():
            record._populate(
                "general_audit_ws_ae598e6.influence",
                "influence_ids",
                "general_audit_ws_bc3e272.influence",
                "influence_id",
            )
            record._populate(
                "general_audit_ws_ae598e6.control",
                "control_ids",
                "general_audit_ws_bc3e272.control",
                "control_id",
            )

    def _populate(self, detail_obj, detail_field, ws_obj, ws_field):
        Detail = self.env[detail_obj]
        Worksheet = self.env[ws_obj]

        for record in self:
            worksheets = Worksheet.search(
                [
                    ("worksheet_id.general_audit_id", "=", record.general_audit_id.id),
                    ("result", "=", "escalated"),
                ]
            )
            if ws_field == "influence_id":
                mapping = {chk.influence_id.id: chk for chk in record[detail_field]}
            else:
                mapping = {chk.control_id.id: chk for chk in record[detail_field]}

            for ws in worksheets:
                if ws.id not in mapping:
                    Detail.create(
                        {
                            "worksheet_id": record.id,
                            ws_field: ws.id,
                            "sequence": ws.sequence,
                        }
                    )

            worksheet_ids = set(worksheets.ids)
            for chk in record[detail_field]:
                if ws_field == "influence_id":
                    if chk.influence_id.id not in worksheet_ids:
                        chk.unlink()
                else:
                    if chk.control_id.id not in worksheet_ids:
                        chk.unlink()

    @ssi_decorator.post_open_action()
    def _10_populate_data(self):
        self.ensure_one()
        self.action_populate()
