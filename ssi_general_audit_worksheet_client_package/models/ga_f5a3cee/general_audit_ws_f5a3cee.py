# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSf5a3cee(models.Model):
    """Worksheet — Data Collection (f5a3cee).

    Tracks the receipt and completeness of client-provided data.  Details
    (``detail_ids``) are auto-populated via ``action_populate_details`` from
    the client's account mapping, one per account type, each holding the data
    lines of the matching Data Collection master items.  ``permanent_ids``
    and ``current_ids`` hold the master items of type Permanent File and
    Current File.  ``primary_ids``
    is the Client Assistance Package, filled from the master items of type
    Primary.  Each line is marked complete once the data or supporting
    documents have been received and attached.  ``reporting_timetable_ids``
    is the manually entered reporting timetable to be followed by the entity.

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
    primary_ids = fields.One2many(
        string="Primary",
        comodel_name="general_audit_ws_f5a3cee.primary",
        inverse_name="worksheet_id",
        help=(
            "Client Assistance Package lines. Lines linked to a Data "
            "Collection master item of type Primary are populated; the "
            "others are entered manually by the user."
        ),
    )
    reporting_timetable_ids = fields.One2many(
        string="Reporting Timetable",
        comodel_name="general_audit_ws_f5a3cee.reporting_timetable",
        inverse_name="worksheet_id",
        help=(
            "Reporting timetable to be followed by the entity, entered "
            "manually by the user."
        ),
    )
    permanent_ids = fields.One2many(
        string="Permanent File",
        comodel_name="general_audit_ws_f5a3cee.permanent",
        inverse_name="worksheet_id",
        help=(
            "Permanent File lines. Lines linked to a Data Collection master "
            "item of type Permanent File are populated; the others are entered "
            "manually by the user."
        ),
    )
    current_ids = fields.One2many(
        string="Current File",
        comodel_name="general_audit_ws_f5a3cee.current",
        inverse_name="worksheet_id",
        help=(
            "Current File lines. Lines linked to a Data Collection master "
            "item of type Current File are populated; the others are entered "
            "manually by the user."
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
        """Populate details, their data lines, file lines and Primary lines."""
        for record in self:
            record._create_details()
            record._populate_detail_lines()
            record._populate_file_lines("permanent_file", "permanent_ids")
            record._populate_file_lines("current_file", "current_ids")
            record._populate_primary_lines()

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
            vals_list = [
                {
                    "detail_id": detail.id,
                    "data_collection_id": master.id,
                    "name": master.name,
                    "category_id": master.category_id.id,
                }
                for master in masters - existing
            ]
            if vals_list:
                Line.create(vals_list)
            detail.line_ids._fill_from_master()
            obsolete = detail.line_ids.filtered(
                lambda line: line.data_collection_id
                and line.data_collection_id not in masters
            )
            obsolete.unlink()

    def _populate_file_lines(self, item_type, field_name):
        """Sync one list of file lines with the master items of one type.

        Only active master items of ``item_type`` are used.  Lines without
        a master item are never touched.

        :param str item_type: type of the master items to use
        :param str field_name: worksheet one2many that holds the lines
        """
        self.ensure_one()
        Master = self.env["general_audit_data_collection"]
        masters = Master.search([("type", "=", item_type)])
        existing = self[field_name].mapped("data_collection_id")
        vals_list = [
            {
                "worksheet_id": self.id,
                "data_collection_id": master.id,
                "description": master.name,
                "category_id": master.category_id.id,
            }
            for master in masters - existing
        ]
        if vals_list:
            self[field_name].create(vals_list)
        self[field_name]._fill_from_master()
        self[field_name].filtered(
            lambda line: line.data_collection_id
            and line.data_collection_id not in masters
        ).unlink()

    def _populate_primary_lines(self):
        """Sync the Primary lines with the Primary master items.

        Only active master items of type Primary are used.  Lines without
        a master item are never touched.
        """
        self.ensure_one()
        Master = self.env["general_audit_data_collection"]
        Primary = self.env["general_audit_ws_f5a3cee.primary"]
        masters = Master.search([("type", "=", "primary")])
        existing = self.primary_ids.mapped("data_collection_id")
        vals_list = [
            {
                "worksheet_id": self.id,
                "data_collection_id": master.id,
                "description": master.name,
            }
            for master in masters - existing
        ]
        if vals_list:
            Primary.create(vals_list)
        self.primary_ids._fill_from_master()
        self.primary_ids.filtered(
            lambda line: line.data_collection_id
            and line.data_collection_id not in masters
        ).unlink()
