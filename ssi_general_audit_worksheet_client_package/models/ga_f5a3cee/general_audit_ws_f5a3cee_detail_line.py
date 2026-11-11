# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWSf5a3ceeDetailLine(models.Model):
    """Data line under a Data Collection detail (f5a3cee).

    Tracks one requested data item for the account type of the parent detail.
    Lines created by migration have no master item."""

    _name = "general_audit_ws_f5a3cee.detail_line"
    _inherit = ["general_audit_ws_f5a3cee.attachment_mixin"]
    _description = "Data Collection (f5a3cee) - Detail Lines"
    _order = "data_collection_code, id"

    detail_id = fields.Many2one(
        string="# Detail",
        comodel_name="general_audit_ws_f5a3cee.detail",
        required=True,
        ondelete="cascade",
        help="Parent detail (account type). Deleting it removes its lines.",
    )
    worksheet_id = fields.Many2one(
        string="# Worksheet",
        related="detail_id.worksheet_id",
        help="Parent Data Collection worksheet.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help=(
            "Name of the requested data. Filled from the Data Collection "
            "item, or entered manually when there is none."
        ),
    )
    data_collection_id = fields.Many2one(
        string="Data Collection Item",
        comodel_name="general_audit_data_collection",
        domain="[('type', '=', 'account_type')]",
        required=False,
        ondelete="restrict",
        help="Data Collection master item that this line refers to.",
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
    date = fields.Date(
        string="Date",
        help="Date associated with the collected data or supporting documents.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_detail_line_2_attachment",
        column1="f5a3cee_detail_line_id",
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
        help="Mark as completed once the data has been collected and reviewed.",
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help="State of the parent worksheet.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create lines, filling the name from the Data Collection item.

        :param list vals_list: values of the lines to create
        :return: the created lines
        :rtype: recordset
        """
        for vals in vals_list:
            if not vals.get("name") and vals.get("data_collection_id"):
                master = self.env["general_audit_data_collection"].browse(
                    vals["data_collection_id"]
                )
                vals["name"] = master.name
            if not vals.get("category_id") and vals.get("data_collection_id"):
                master = self.env["general_audit_data_collection"].browse(
                    vals["data_collection_id"]
                )
                vals["category_id"] = master.category_id.id
        return super().create(vals_list)

    @api.onchange("data_collection_id")
    def onchange_name(self):
        """Fill the name from the selected Data Collection item."""
        if self.data_collection_id:
            self.name = self.data_collection_id.name
            self.category_id = self.data_collection_id.category_id

    @api.constrains("detail_id", "data_collection_id", "name")
    def _check_duplicate(self):
        """Reject a repeated Data Collection item or name.

        A Data Collection item may be used once per worksheet, and a name
        once per detail.  The message tells for which account type it is
        already used.

        :raises ValidationError: if the Data Collection item is used by
            another line of the worksheet, or the name by another line of
            the same detail.
        """
        for record in self:
            detail = record.detail_id
            if record.data_collection_id:
                used = (detail.worksheet_id.detail_ids.line_ids - record).filtered(
                    lambda line: line.data_collection_id == record.data_collection_id
                )[:1]
                if used:
                    raise ValidationError(
                        _(
                            "Data Collection %(code)s is already used for "
                            "account type %(account_type)s."
                        )
                        % {
                            "code": record.data_collection_id.code,
                            "account_type": used.detail_id.account_client_type_id.name,
                        }
                    )
            name = (record.name or "").strip().lower()
            used = (detail.line_ids - record).filtered(
                lambda line: (line.name or "").strip().lower() == name
            )[:1]
            if used:
                raise ValidationError(
                    _(
                        'Name "%(name)s" is already used in this detail for '
                        "account type %(account_type)s."
                    )
                    % {
                        "name": record.name,
                        "account_type": detail.account_client_type_id.name,
                    }
                )

    def _fill_from_master(self):
        """Fill the empty name and category from the Data Collection item.

        Values that are already filled are never overwritten.
        """
        for record in self.filtered("data_collection_id"):
            master = record.data_collection_id
            vals = {}
            if not record.name:
                vals["name"] = master.name
            if not record.category_id:
                vals["category_id"] = master.category_id.id
            if vals:
                record.write(vals)
