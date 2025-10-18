# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe78a3c6(models.Model):
    _name = "general_audit_ws_e78a3c6"
    _description = "Structure Organization and Responsibilities (e78a3c6)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_e78a3c6"
    )

    organtization_structure_ids = fields.One2many(
        string="Organization Structures",
        comodel_name="general_audit_ws_e78a3c6.organization_structure",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Collection of organization structure records linked to this worksheet. "
            "Editable only when the worksheet is in the Open state. "
            "Use this field to capture hierarchy, roles, and reporting lines."
        ),
    )
    organization_structure_image = fields.Image(
        string="Organization Structure Image",
        max_width=1920,
        max_height=1920,
        help=(
            "Organization structure chart image used for documentation and reporting. "
            "Maximum size is 1920x1920 pixels; larger images will be resized. "
            "Recommended formats: PNG or JPEG."
        ),
    )
