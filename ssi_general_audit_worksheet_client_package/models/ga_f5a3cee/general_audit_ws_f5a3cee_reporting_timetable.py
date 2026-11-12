# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWsF5a3ceeReportingTimetable(models.Model):
    """Reporting timetable line for the Data Collection worksheet (f5a3cee).

    Tracks a manually entered reporting deliverable (free-text description
    plus an optional due/received date).  Rows may be added by the user or
    populated from the Data Collection master items of type Others.
    """

    _name = "general_audit_ws_f5a3cee.reporting_timetable"
    _inherit = ["general_audit_ws_f5a3cee.attachment_mixin"]
    _description = "Data Collection (f5a3cee) - Reporting Timetable"
    _order = "data_collection_code, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_f5a3cee",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent Data Collection worksheet. "
            "Deleting the worksheet will remove its reporting timetable "
            "lines."
        ),
    )
    data_collection_id = fields.Many2one(
        string="Data Collection Item",
        comodel_name="general_audit_data_collection",
        domain="[('type', '=', 'others')]",
        ondelete="restrict",
        help="Data Collection master item (type Others) of this line, if any.",
    )
    data_collection_code = fields.Char(
        string="Data Collection Code",
        related="data_collection_id.code",
        store=True,
        help="Code of the Data Collection item, used to sort the lines.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="general_audit_data_collection_category",
        ondelete="restrict",
        help=(
            "Category of the requested data. Filled from the Data "
            "Collection item, and can be chosen manually."
        ),
    )
    description = fields.Char(
        string="Description",
        required=True,
        help="Free-text description of the reporting deliverable.",
    )
    date = fields.Date(
        string="Date",
        required=False,
        help="Date associated with the reporting deliverable.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_reporting_timetable_2_attachment",
        column1="f5a3cee_reporting_timetable_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_f5a3cee'), "
        "('res_id', '=', worksheet_id)]",
        help=(
            "Files attached as supporting evidence. "
            "Only attachments linked to this worksheet can be selected."
        ),
    )
    complete_ok = fields.Boolean(
        string="Completed",
        default=False,
        help=(
            "Mark as completed once the reporting deliverable described "
            "by this line has been received and reviewed."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create lines, filling the category from the Data Collection item.

        :param list vals_list: values of the lines to create
        :return: the created lines
        :rtype: recordset
        """
        for vals in vals_list:
            if not vals.get("category_id") and vals.get("data_collection_id"):
                master = self.env["general_audit_data_collection"].browse(
                    vals["data_collection_id"]
                )
                vals["category_id"] = master.category_id.id
        return super().create(vals_list)

    @api.onchange("data_collection_id")
    def onchange_description(self):
        """Fill the description from the selected Data Collection item."""
        if self.data_collection_id:
            self.description = self.data_collection_id.name
            self.category_id = self.data_collection_id.category_id

    @api.constrains("worksheet_id", "data_collection_id")
    def _check_duplicate_data_collection(self):
        """Reject a repeated Data Collection item in one worksheet.

        :raises ValidationError: if another line of the same worksheet has
            the same Data Collection item.
        """
        for record in self.filtered("data_collection_id"):
            siblings = record.worksheet_id.reporting_timetable_ids - record
            if record.data_collection_id in siblings.data_collection_id:
                raise ValidationError(
                    _("Data Collection %s is already used in this worksheet.")
                    % record.data_collection_id.code
                )

    def _fill_from_master(self):
        """Fill the empty description and category from the master item.

        Values that are already filled are never overwritten.
        """
        for record in self.filtered("data_collection_id"):
            master = record.data_collection_id
            vals = {}
            if not record.description:
                vals["description"] = master.name
            if not record.category_id:
                vals["category_id"] = master.category_id.id
            if vals:
                record.write(vals)
