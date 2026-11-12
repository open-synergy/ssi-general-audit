# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class GeneralAuditWSf5a3ceeAttachmentUpload(models.TransientModel):
    """Upload files to a line of the Data Collection worksheet (f5a3cee).

    Opened from a button in the list of a data line or a reporting timetable
    line.  Uploaded files are linked to the line and, through the attachment
    mixin, to the worksheet record itself.
    """

    _name = "general_audit_ws_f5a3cee_attachment_upload"
    _description = "Data Collection (f5a3cee) - Upload Attachment"

    attachment_ids = fields.Many2many(
        string="Files",
        comodel_name="ir.attachment",
        relation="rel_ga_f5a3cee_attachment_upload_2_attachment",
        column1="wizard_id",
        column2="attachment_id",
        help="Files to attach to the line.",
    )

    def _get_line(self):
        """Return the line the wizard was opened from.

        :return: the data line or reporting timetable line
        :rtype: recordset
        :raises UserError: if the line is not saved yet
        """
        self.ensure_one()
        context = self.env.context
        model = context.get("active_model")
        res_id = context.get("active_id")
        if model not in (
            "general_audit_ws_f5a3cee.detail_line",
            "general_audit_ws_f5a3cee.reporting_timetable",
        ):
            raise UserError(_("This wizard must be opened from a data line."))
        line = self.env[model].browse(res_id).exists()
        if not line:
            raise UserError(_("Save the line first, then upload the files."))
        return line

    def action_submit(self):
        """Link the uploaded files to the line.

        The attachment mixin binds the files to the worksheet record.

        :return: action closing the wizard
        :rtype: dict
        """
        self.ensure_one()
        line = self._get_line()
        if self.attachment_ids:
            line.write({"attachment_ids": [(4, att.id) for att in self.attachment_ids]})
        return {"type": "ir.actions.act_window_close"}
