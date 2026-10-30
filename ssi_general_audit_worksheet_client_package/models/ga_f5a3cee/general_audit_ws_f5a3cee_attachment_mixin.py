# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class GeneralAuditWsF5a3ceeAttachmentMixin(models.AbstractModel):
    """Link orphan attachments of f5a3cee lines to the parent worksheet.

    Attachments added through the ``many2many_tags`` widget are created
    without ``res_model`` and ``res_id``, so Odoo only lets their creator
    read them.  This mixin binds such attachments to the parent worksheet
    so every user entitled to the worksheet can read them.
    """

    _name = "general_audit_ws_f5a3cee.attachment_mixin"
    _description = "Data Collection (f5a3cee) - Attachment Link Mixin"

    @api.model_create_multi
    def create(self, vals_list):
        """Create records and link orphan attachments to the worksheet.

        :param list vals_list: values of the records to create
        :return: the created records
        :rtype: recordset
        """
        records = super().create(vals_list)
        if any("attachment_ids" in vals for vals in vals_list):
            records._link_orphan_attachments()
        return records

    def write(self, vals):
        """Write values and link orphan attachments to the worksheet.

        :param dict vals: values to write
        :return: result of the parent ``write``
        :rtype: bool
        """
        result = super().write(vals)
        if "attachment_ids" in vals:
            self._link_orphan_attachments()
        return result

    def _link_orphan_attachments(self):
        """Bind attachments without ``res_id`` to the parent worksheet.

        Attachments already linked to another record are left untouched,
        and ``res_field`` is never modified.  The write runs as superuser
        so it does not depend on who created the attachment.
        """
        for record in self.sudo():
            orphans = record.attachment_ids.filtered(lambda att: not att.res_id)
            if orphans:
                orphans.write(
                    {
                        "res_model": "general_audit_ws_f5a3cee",
                        "res_id": record.worksheet_id.id,
                    }
                )
