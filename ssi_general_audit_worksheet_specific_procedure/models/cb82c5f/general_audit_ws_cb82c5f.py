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

    adjustment_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_cb82c5f.adjustment_detail",
        inverse_name="worksheet_id",
        string="Need Adjustment Details",
        help="Details of subsequent events that need adjustment",
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    non_adjustment_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_cb82c5f.non_adjustment_detail",
        inverse_name="worksheet_id",
        string="Need Non-Adjustment Details",
        help="Details of subsequent events that do not need adjustment",
        readonly=True,
        states={"open": [("readonly", False)]},
    )

    def action_load_adjustment_detail(self):
        for record in self.sudo():
            record._load_adjustment_detail()

    def action_load_non_adjustment_detail(self):
        for record in self.sudo():
            record._load_non_adjustment_detail()

    def _load_non_adjustment_detail(self):
        self.ensure_one()
        SubsequentEvent = self.env["general_audit_subsequent_event"]
        existing_events = self.non_adjustment_detail_ids.mapped("subsequent_event_id")
        all_subsequent_events = SubsequentEvent.search(
            [("need_adjustment", "=", False)]
        )
        to_add_events = all_subsequent_events - existing_events
        to_remove_details = existing_events - all_subsequent_events

        # Add new details for subsequent events not yet in the worksheet
        for event in to_add_events:
            self.env["general_audit_ws_cb82c5f.non_adjustment_detail"].create(
                {
                    "worksheet_id": self.id,
                    "subsequent_event_id": event.id,
                }
            )

        # Remove details for subsequent events no longer applicable
        details_to_remove = self.non_adjustment_detail_ids.filtered(
            lambda d: d.subsequent_event_id in to_remove_details
        )
        if details_to_remove:
            details_to_remove.unlink()

    def _load_adjustment_detail(self):
        self.ensure_one()
        SubsequentEvent = self.env["general_audit_subsequent_event"]
        existing_events = self.adjustment_detail_ids.mapped("subsequent_event_id")
        all_subsequent_events = SubsequentEvent.search([("need_adjustment", "=", True)])
        to_add_events = all_subsequent_events - existing_events
        to_remove_details = existing_events - all_subsequent_events

        # Add new details for subsequent events not yet in the worksheet
        for event in to_add_events:
            self.env["general_audit_ws_cb82c5f.adjustment_detail"].create(
                {
                    "worksheet_id": self.id,
                    "subsequent_event_id": event.id,
                }
            )

        # Remove details for subsequent events no longer applicable
        details_to_remove = self.adjustment_detail_ids.filtered(
            lambda d: d.subsequent_event_id in to_remove_details
        )
        if details_to_remove:
            details_to_remove.unlink()
