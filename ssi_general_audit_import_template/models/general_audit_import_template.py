# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class GeneralAuditImportTemplate(models.Model):
    """CSV import template of a General Audit target model.

    Master data that lets an administrator define the columns of the CSV
    file a user must prepare before importing data into the target
    model. A button creates a server action bound to the target model,
    so the user can download the template from the Action menu of that
    model.
    """

    _name = "general_audit_import_template"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Import Template"

    code = fields.Char(
        default="/",
    )
    model_id = fields.Many2one(
        string="Target Model",
        comodel_name="ir.model",
        required=True,
        ondelete="cascade",
        help="Model whose Action menu offers the template download.",
    )
    file_name = fields.Char(
        string="File Name",
        required=True,
        default="import_template.csv",
        help="Name of the CSV file the user downloads.",
    )
    delimiter = fields.Selection(
        string="Delimiter",
        selection=[
            (",", "Comma"),
            (";", "Semicolon"),
        ],
        required=True,
        default=",",
        help="Character that separates the columns in the CSV file.",
    )
    has_header = fields.Boolean(
        string="Has Header",
        default=True,
        help="Write the column titles as the first row of the CSV file.",
    )
    line_ids = fields.One2many(
        string="Columns",
        comodel_name="general_audit_import_template.line",
        inverse_name="template_id",
        help="Columns of the CSV file, in the order they are written.",
    )
    server_action_id = fields.Many2one(
        string="Server Action",
        comodel_name="ir.actions.server",
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Server action that offers the download in the Action menu.",
    )

    @api.constrains("model_id", "server_action_id")
    def _check_model_id(self):
        """Reject a target model change while the server action exists.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_model_id_condition():
                error_message = """
Document Type: %s
Context: Change target model
Database ID: %s
Problem: Target model can not change while the server action exists
Solution: Remove the server action first
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_model_id_condition(self):
        """Tell whether the target model matches the server action.

        Extension point: override to relax the rule without touching
        the error message.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.server_action_id:
            return True
        return self.server_action_id.model_id == self.model_id

    def write(self, vals):
        """Rename the server action together with its template.

        Also applies to the writes of the data loader on module update,
        so a renamed seed template renames its server action.

        :param vals: the values to write
        :return: result of the parent ``write``
        """
        result = super().write(vals)
        if "name" in vals:
            for record in self.sudo():
                server_action = record.server_action_id
                name = record._get_server_action_name()
                if server_action and server_action.name != name:
                    server_action.write({"name": name})
        return result

    def unlink(self):
        """Delete the templates together with their server actions.

        Overridden so no server action stays in the Action menu of the
        target model after its template is gone.

        :return: result of the parent ``unlink``
        """
        for record in self.sudo():
            if record.server_action_id:
                record.server_action_id.unlink()
        return super().unlink()

    def action_create_server_action(self):
        """Create the download server action of this template.

        After the click the Action menu of the target model offers
        "Download Template: <name>".
        """
        for record in self.sudo():
            record._create_server_action()

    def _create_server_action(self):
        """Create the ``ir.actions.server`` bound to the target model.

        The action runs ``action_download`` of this template and is
        stored in ``server_action_id``.

        :raises UserError: when the server action already exists
        """
        self.ensure_one()
        if self.server_action_id:
            error_message = """
Document Type: %s
Context: Create server action
Database ID: %s
Problem: Server action already exists
Solution: Remove the server action first
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))
        server_action = self.env["ir.actions.server"].create(
            self._prepare_server_action()
        )
        self.write({"server_action_id": server_action.id})

    def _get_server_action_name(self):
        """Build the name of the download server action of this template.

        :return: the string "Download Template: <name>"
        """
        self.ensure_one()
        return _("Download Template: ") + (self.name or "")

    def _prepare_server_action(self):
        """Build the ``ir.actions.server`` values for this template.

        Extension point: override in a glue module to change the action.

        :return: dict of ``ir.actions.server`` values
        """
        self.ensure_one()
        code = 'action = env["%s"].browse(%s).action_download()' % (
            self._name,
            self.id,
        )
        return {
            "name": self._get_server_action_name(),
            "model_id": self.model_id.id,
            "binding_model_id": self.model_id.id,
            "binding_type": "action",
            "state": "code",
            "code": code,
        }

    def action_remove_server_action(self):
        """Delete the download server action of this template.

        The download entry disappears from the Action menu of the
        target model.
        """
        for record in self.sudo():
            record._remove_server_action()

    def _remove_server_action(self):
        """Delete the server action and clear ``server_action_id``."""
        self.ensure_one()
        server_action = self.server_action_id
        self.write({"server_action_id": False})
        server_action.unlink()

    def action_download(self):
        """Return the action that downloads the template file.

        Called by the server action, not by a form button. A CSV file
        is generated: the header row holds the column titles when
        ``has_header`` is set; one example row holds the example
        values.

        :return: an ``ir.actions.act_url`` dict to ``/web/content/``
        """
        self.ensure_one()
        output = io.StringIO()
        writer = csv.writer(output, delimiter=self.delimiter, lineterminator="\n")
        lines = self.line_ids.sorted(lambda r: (r.sequence, r.id))
        if self.has_header:
            writer.writerow([line.name for line in lines])
        writer.writerow([line.example_value or "" for line in lines])
        attachment = self.env["ir.attachment"].create(
            {
                "name": self.file_name,
                "type": "binary",
                "datas": base64.b64encode(output.getvalue().encode("utf-8")),
                "res_model": self._name,
                "res_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "self",
        }
