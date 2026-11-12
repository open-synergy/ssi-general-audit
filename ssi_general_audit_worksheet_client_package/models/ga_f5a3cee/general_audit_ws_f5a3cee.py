# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSf5a3cee(models.Model):
    """Worksheet — Data Collection (f5a3cee).

    Tracks the receipt and completeness of client-provided data.  Details
    (``detail_ids``) are auto-populated via ``action_populate_details`` from
    the client's account mapping, one per account type, each holding the data
    lines of the matching Data Collection master items.  ``reporting_timetable_ids``
    also holds the master items that are not tied to an account type.  Each line is
    marked complete once the data or supporting documents have been received
    and attached.

    This worksheet gives the engagement team a consolidated view of outstanding
    data requests and ensures no account type is overlooked before fieldwork
    begins.

    ISA/SA references: ISA 500/SA 500 (Audit Evidence);
    ISA 315/SA 315 (Identifying and Assessing Risks).
    """

    _name = "general_audit_ws_f5a3cee"
    _description = "Data Collection (f5a3cee)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_client_package." "worksheet_type_f5a3cee"
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f5a3cee.detail",
        inverse_name="worksheet_id",
        help=(
            "Detail lines automatically populated from the client's " "account mapping."
        ),
    )
    reporting_timetable_ids = fields.One2many(
        string="Reporting Timetable",
        comodel_name="general_audit_ws_f5a3cee.reporting_timetable",
        inverse_name="worksheet_id",
        help=(
            "Reporting deliverable and other data lines. Lines linked to a "
            "Data Collection master item are populated; the others are "
            "entered manually by the user."
        ),
    )

    def _create_details_data(self, mapping):
        self.ensure_one()
        data = {
            "worksheet_id": self.id,
            "account_client_type_id": mapping.id,
        }
        return data

    def _update_details_data(self, mapping):
        self.ensure_one()
        data = {
            "account_client_type_id": mapping.id,
        }
        return data

    def action_populate_details(self):
        """Populate details, their data lines and the other data lines."""
        for record in self:
            record._create_details()
            record._populate_detail_lines()
            record._populate_other_lines()

    def _create_details(self):
        """Create one detail per account type in the client's mapping."""
        self.ensure_one()
        Detail = self.env["general_audit_ws_f5a3cee.detail"]
        AccMapping = self.env["client_account_mapping"]

        criteria = [("partner_id", "=", self.partner_id.id)]

        acc_mapping_type_ids = AccMapping.search(criteria).mapped("detail_ids").type_id
        mapping = {chk.account_client_type_id.id: chk for chk in self.detail_ids}

        if acc_mapping_type_ids:
            for acc_type in acc_mapping_type_ids:
                if acc_type.id not in mapping:
                    Detail.create(self._create_details_data(acc_type))
                else:
                    mapping[acc_type.id].write(self._update_details_data(acc_type))

            for chk in self.detail_ids:
                if chk.account_client_type_id.id not in acc_mapping_type_ids.ids:
                    chk.unlink()

    def _populate_detail_lines(self):
        """Sync the data lines of every detail with the master items.

        A line is kept when its master is still active, of type
        ``account_type`` and of the detail's account type.  Lines without a
        master are never touched.
        """
        self.ensure_one()
        Master = self.env["general_audit_data_collection"]
        Line = self.env["general_audit_ws_f5a3cee.detail_line"]
        for detail in self.detail_ids:
            masters = Master.search(
                [
                    ("type", "=", "account_type"),
                    ("account_type_id", "=", detail.account_client_type_id.id),
                ]
            )
            existing = detail.line_ids.mapped("data_collection_id")
            for master in masters - existing:
                Line.create(
                    {
                        "detail_id": detail.id,
                        "data_collection_id": master.id,
                        "name": master.name,
                    }
                )
            detail.line_ids._fill_from_master()
            obsolete = detail.line_ids.filtered(
                lambda line: line.data_collection_id
                and line.data_collection_id not in masters
            )
            obsolete.unlink()

    def _populate_other_lines(self):
        """Sync the timetable lines with the master items of type others.

        Lines without a master item are never touched.
        """
        self.ensure_one()
        Master = self.env["general_audit_data_collection"]
        Timetable = self.env["general_audit_ws_f5a3cee.reporting_timetable"]
        masters = Master.search([("type", "=", "others")])
        existing = self.reporting_timetable_ids.mapped("data_collection_id")
        for master in masters - existing:
            Timetable.create(
                {
                    "worksheet_id": self.id,
                    "data_collection_id": master.id,
                    "description": master.name,
                    "category_id": master.category_id.id,
                }
            )
        self.reporting_timetable_ids._fill_from_master()
        self.reporting_timetable_ids.filtered(
            lambda line: line.data_collection_id
            and line.data_collection_id not in masters
        ).unlink()
