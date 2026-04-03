# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSAE11F7EOtherProvidedService(models.Model):
    """Other provided service entry within the Main Business Activity worksheet.

    Documents outsourced services or third-party arrangements relevant to the
    entity's operations (e.g., shared service centres, IT outsourcing, payroll
    processing). Per ISA 402 / SA 402, auditors must understand service
    organisation arrangements and their impact on internal controls.
    """

    _name = "general_audit_ws_ae11f7e.other_provided_service"
    _description = "Worksheet ae11f7e - Other Provided Service"
    _order = "worksheet_id, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_ae11f7e",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent worksheet. "
            "This entry will be removed if the worksheet is deleted."
        ),
    )
    name = fields.Char(
        string="Service",
        required=True,
        help="Name of the service provided. This field identifies the service.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        help=(
            "Business partner associated with this service, such as a customer, "
            "vendor, or other related party."
        ),
    )
    summary = fields.Text(
        string="Summary",
        help="Brief description of the service and any relevant context or notes.",
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_ae11f7e_provided_service_2_account_type",
        column1="prev_audit_id",
        column2="type_id",
        required=True,
        help=(
            "Standard account types related to this item. Used to link the entry to "
            "relevant accounts."
        ),
    )
