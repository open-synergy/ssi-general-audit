# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSddf034cContact(models.Model):
    _name = "general_audit_ws_ddf034c.contact"
    _description = "General Information and Legal Aspec (ddf034c) - " "Client Contacts"
    _order = "sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ddf034c",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the ddf034c worksheet this contact belongs to. "
            "If the worksheet is deleted, related contacts are removed (cascade)."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
        help=(
            "Controls the display order of contacts within the worksheet. "
            "Lower values appear first."
        ),
    )
    worksheet_partner_id = fields.Many2one(
        string="Worksheet Partner",
        related="worksheet_id.partner_id",
        help=(
            "Customer/partner company associated with the worksheet. "
            "Used to filter available contact persons."
        ),
    )
    state = fields.Selection(
        related="worksheet_id.state",
        help=(
            "Status of the parent worksheet. "
            "Read-only and synchronized from the worksheet."
        ),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain="[('is_company', '=', False), ('parent_id', '=', worksheet_partner_id)]",
        ondelete="restrict",
        help=(
            "Select the contact person from the worksheet's partner company. "
            "Only individual contacts under the partner are allowed."
        ),
    )
    contact_name = fields.Char(
        string="Name",
        help=(
            "Contact person's name. "
            "Auto-filled when a Partner is selected but can be edited."
        ),
    )
    contact_position = fields.Char(
        string="Position",
        help=(
            "Job title/position of the contact person (e.g., Finance Manager). "
            "Auto-filled from Partner when available."
        ),
    )
    contact_phone = fields.Char(
        string="Phone",
        help=(
            "Office phone number of the contact person. "
            "Auto-filled from Partner when available."
        ),
    )
    contact_mobile = fields.Char(
        string="Mobile",
        help=(
            "Mobile phone number of the contact person. "
            "Auto-filled from Partner when available."
        ),
    )
    contact_email = fields.Char(
        string="Email",
        help=(
            "Email address of the contact person. "
            "Auto-filled from Partner when available."
        ),
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_name(self):
        self.contact_name = ""
        if self.partner_id:
            self.contact_name = self.partner_id.name

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_position(self):
        self.contact_position = ""
        if self.partner_id:
            self.contact_position = self.partner_id.function

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_phone(self):
        self.contact_phone = ""
        if self.partner_id:
            self.contact_phone = self.partner_id.phone

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_mobile(self):
        self.contact_mobile = ""
        if self.partner_id:
            self.contact_mobile = self.partner_id.mobile

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_email(self):
        self.contact_email = ""
        if self.partner_id:
            self.contact_email = self.partner_id.email
