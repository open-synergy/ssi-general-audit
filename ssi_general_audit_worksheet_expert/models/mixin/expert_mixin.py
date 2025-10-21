# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class MixinExpert(models.AbstractModel):
    _name = "mixin.expert"
    _description = "Mixin for Expert"
    _detail_model_name = ""
    _factor_model_name = ""
    _expert_create_page = True
    _expert_create_header = True
    _expert_header_xpath = "//group[@name='header']"
    _expert_header_position = "after"
    _expert_page_xpath = "//page[@name='note']"
    _expert_position = "before"
    EXPERT_STATES = {
        "open": [("readonly", False), ("required", True)],
    }

    expert_name = fields.Char(
        string="Name of Expert (Individual/Organization)",
        readonly=True,
        states=EXPERT_STATES,
        help="Full name of the expert, either individual or organization.",
    )
    expert_type_id = fields.Many2one(
        string="Field of Expertise",
        comodel_name="general_audit_expert_type",
        readonly=True,
        states=EXPERT_STATES,
        help="Area of specialization or professional expertise of the expert.",
    )
    expert_account_ids = fields.Many2many(
        string="Significant Accounts",
        comodel_name="client_account_type",
        readonly=True,
        states=EXPERT_STATES,
        domain="[('id', 'in', account_type_ids)]",
        help=(
            "Accounts or disclosures that are significantly "
            "influenced by the expert's work."
        ),
    )
    contracting_party = fields.Char(
        string="Party Entering into Contract with the Expert",
        readonly=True,
        states=EXPERT_STATES,
        help="Entity or individual who entered into a contract with the expert.",
    )
    detail_ids = fields.One2many(
        comodel_name="mixin.expert.detail",
        inverse_name="expert_id",
        string="Details",
        readonly=True,
        states=EXPERT_STATES,
        help="Expert values generated from master items for this document.",
    )

    def _get_expert_field_name(self):
        """Nama field One2many untuk expert"""
        return "detail_ids"

    def _get_expert_extra_vals(self, item):
        """Override untuk menambahkan field tambahan ke expert"""
        return {}

    @ssi_decorator.insert_on_form_view()
    def _expert_insert_form_element(self, view_arch):
        if self._expert_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_general_audit_worksheet_expert.expert_page",
                xpath=self._expert_page_xpath,
                position=self._expert_position,
            )
        if self._expert_create_header:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_general_audit_worksheet_expert.expert_header",
                xpath=self._expert_header_xpath,
                position=self._expert_header_position,
            )
        return view_arch

    def action_populate_expert(self):
        """Generic method untuk populate expert dari master items"""
        if self._detail_model_name and self._factor_model_name:
            Detail = self.env[self._detail_model_name]
            Factor = self.env[self._factor_model_name]

            for record in self:
                factors = Factor.search([])
                expert_field = self._get_expert_field_name()

                expert_map = {chk.factor_id.id: chk for chk in record[expert_field]}

                for factor in factors:
                    if factor.id not in expert_map:
                        Detail.create(
                            {
                                "expert_id": record.id,
                                "factor_id": factor.id,
                                "sequence": factor.sequence,
                                **self._get_expert_extra_vals(factor),
                            }
                        )

                factor_ids = set(factors.ids)
                for chk in record[expert_field]:
                    if chk.factor_id.id not in factor_ids:
                        chk.unlink()
        else:
            return True

    @ssi_decorator.pre_confirm_check()
    def _10_check_expert_type_id(self):
        self.ensure_one()
        criteria = [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
            ("expert_type_id", "=", self.expert_type_id.id),
            ("id", "!=", self.id),
        ]
        check = self.search(criteria)
        if check:
            error_message = """
            Context: Confirmation for %s
            Database ID: %s
            Problem: Expert Type %s is already used for General Audit %s.
            """ % (
                self.type_id.display_name,
                self.id,
                self.expert_type_id.display_name,
                self.display_name,
            )
            raise ValidationError(_(error_message))
