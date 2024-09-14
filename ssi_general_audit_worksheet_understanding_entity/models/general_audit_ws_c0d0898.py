# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSc0d0898(models.Model):
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
