# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSe78a3c6OrganizationStructure(models.Model):
    """Organization unit line within the Org Structure worksheet.

    Represents a single organizational unit (department, division, team) in
    the entity's hierarchy. Captures the unit's name and its responsibilities.
    Used together with the organization structure chart image to give the
    auditor a complete picture of governance and segregation of duties
    (ISA 315, ISA 265).
    """

    _name = "general_audit_ws_e78a3c6.organization_structure"
    _description = "Worksheet e78a3c6 - Organization Structure"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_e78a3c6",
        required=True,
        ondelete="cascade",
        help=(
            "Reference to the parent e78a3c6 worksheet that this line belongs to. "
            "Groups organization structure entries under a single worksheet. "
            "If the worksheet is deleted, related entries are removed (cascade)."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help=(
            "Controls the display order of organization structure entries. "
            "Lower values appear first."
        ),
    )
    name = fields.Char(
        string="Unit of Organization",
        required=True,
        help=(
            "Name of the organizational unit (e.g., department, team, function). "
            "Use a clear and concise title."
        ),
    )
    responsibility = fields.Text(
        string="Responsiblity",
        required=True,
        help=(
            "Describe the unit's responsibilities and key duties. "
            "Include scope, decision rights, and reporting obligations."
        ),
    )
