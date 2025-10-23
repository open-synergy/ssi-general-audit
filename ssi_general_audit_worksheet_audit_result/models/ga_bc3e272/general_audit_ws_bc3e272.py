# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSbc3e272(models.Model):
    _name = "general_audit_ws_bc3e272"
    _description = "Audit Result Discussion (bc3e272)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_bc3e272"

    influence_ids = fields.One2many(
        string="Findings That Influence Opinion",
        comodel_name="general_audit_ws_bc3e272.influence",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Lines referencing 'Findings That Influence Opinion' to be discussed "
            "and tracked within this worksheet. Editable when state is Open."
        ),
    )
    control_ids = fields.One2many(
        string="Control Deficiencies",
        comodel_name="general_audit_ws_bc3e272.control",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "Lines referencing 'Control Deficiencies' to be discussed and tracked "
            "within this worksheet. Editable when state is Open."
        ),
    )

    def action_populate(self):
        for record in self.sudo():
            record._populate(
                "general_audit_ws_bc3e272.influence",
                "influence_ids",
                "general_audit_ws_a0319a2.detail",
            )
            record._populate(
                "general_audit_ws_bc3e272.control",
                "control_ids",
                "general_audit_ws_d33420f.detail",
            )

    def _populate(self, detail_obj, detail_field, ws_obj):
        Detail = self.env[detail_obj]
        Worksheet = self.env[ws_obj]

        for record in self:
            worksheets = Worksheet.search([])
            mapping = {chk.detail_id.id: chk for chk in record[detail_field]}

            for ws in worksheets:
                if ws.id not in mapping:
                    Detail.create(
                        {
                            "worksheet_id": record.id,
                            "detail_id": ws.id,
                            "sequence": ws.sequence,
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
