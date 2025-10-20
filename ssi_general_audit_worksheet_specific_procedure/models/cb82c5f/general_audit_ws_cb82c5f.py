# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWScb82c5f(models.Model):
    _name = "general_audit_ws_cb82c5f"
    _description = "Subsequent Event (cb82c5f)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_specific_procedure." "worksheet_type_cb82c5f"
    )

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_cb82c5f.detail",
        inverse_name="worksheet_id",
        string="Details",
        help="Details of subsequent events evaluated in this worksheet",
        readonly=True,
        states={"draft": [("readonly", False)], "open": [("readonly", False)]},
    )

    def action_load_detail(self):
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        self.ensure_one()
        SubsequentEvent = self.env["general_audit_subsequent_event"]
        existing_events = self.detail_ids.mapped("subsequent_event_id")
        all_subsequent_events = SubsequentEvent.search([])
        to_add_events = all_subsequent_events - existing_events
        to_remove_details = existing_events - all_subsequent_events

        # Add new details for subsequent events not yet in the worksheet
        for event in to_add_events:
            self.env["general_audit_ws_cb82c5f.detail"].create(
                {
                    "worksheet_id": self.id,
                    "subsequent_event_id": event.id,
                }
            )

        # Remove details for subsequent events no longer applicable
        details_to_remove = self.detail_ids.filtered(
            lambda d: d.subsequent_event_id in to_remove_details
        )
        if details_to_remove:
            details_to_remove.unlink()
