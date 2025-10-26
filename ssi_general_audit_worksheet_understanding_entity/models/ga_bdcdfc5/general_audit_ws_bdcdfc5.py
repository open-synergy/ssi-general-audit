# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWSbdcdfc5(models.Model):
    _name = "general_audit_ws_bdcdfc5"
    _description = "Understanding of the business environment (bdcdfc5)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_understanding_entity." "worksheet_type_bdcdfc5"
    )

    business_environment_id = fields.Many2one(
        string="Business Environment",
        comodel_name="general_audit_business_environment",
        required=False,
        readonly=True,
        ondelete="restrict",
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
        help=(
            "Business environment selected for this worksheet. "
            "Defines the context for assessing risks, controls, and processes. "
            "Editable only when the worksheet is Open and required in that state."
        ),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_bdcdfc5.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "Detailed assessment lines related to this worksheet. "
            "Add or update details when the worksheet status is Open."
        ),
    )

    @ssi_decorator.pre_confirm_check()
    def _10_check_business_environment(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("business_environment_id", "=", self.business_environment_id.id),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Business environment %s is already used for General Audit %s.
            """ % (
                self.type_id.display_name,
                self.id,
                self.business_environment_id.display_name,
                self.display_name,
            )
            raise ValidationError(_(error_message))
