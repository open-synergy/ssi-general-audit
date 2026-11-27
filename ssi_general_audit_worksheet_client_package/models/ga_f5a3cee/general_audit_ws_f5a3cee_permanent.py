# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWsF5a3ceePermanent(models.Model):
    """Permanent File line of the Data Collection worksheet (f5a3cee).

    Tracks one requested item of type Permanent File.  Rows are populated from
    the Data Collection master items of that type, or added by the user
    without a master item.
    """

    _name = "general_audit_ws_f5a3cee.permanent"
    _inherit = ["general_audit_ws_f5a3cee.file_line_mixin"]
    _description = "Data Collection (f5a3cee) - Permanent File"
    _worksheet_field = "permanent_ids"

    data_collection_id = fields.Many2one(
        domain="[('type', '=', 'permanent_file')]",
        help="Data Collection master item (type Permanent File) of this line, if any.",
    )
    attachment_ids = fields.Many2many(
        string="Attachments",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_permanent_2_attachment",
        column1="f5a3cee_permanent_id",
        column2="attachment_id",
        domain="[('res_model', '=', 'general_audit_ws_f5a3cee'), "
        "('res_id', '=', worksheet_id)]",
        help=(
            "Files attached as supporting evidence. "
            "Only attachments linked to this worksheet can be selected."
        ),
    )
