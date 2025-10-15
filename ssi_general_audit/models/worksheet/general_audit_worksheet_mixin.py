# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAuditWorksheetMixin(models.AbstractModel):
    _name = "general_audit_worksheet_mixin"
    _description = "General Audit Worksheet Mixin"
    _inherits = {
        "general_audit_worksheet": "worksheet_id",
    }
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_cancel",
    ]
    _order = "general_audit_id, parent_type_id, id"
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _multiple_approval_xpath_reference = "//page[@name='note']"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "open_ok" "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_worksheet",
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    @api.model
    def _default_type_id(self):
        result = False
        if self._type_xml_id:
            result = self.env.ref(self._type_xml_id)
        return result

    type_id = fields.Many2one(
        string="Type",
        comodel_name="general_audit_worksheet_type",
        default=lambda self: self._default_type_id(),
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "type_id",
        "type_id.standard_item_ids",
    )
    def _compute_standard_item_ids(self):
        for record in self:
            record.standard_item_ids = record.type_id.standard_item_ids.ids

    standard_item_ids = fields.Many2many(
        string="Relevant Audit Standard Items",
        comodel_name="general_audit_standard_audit",
        compute="_compute_standard_item_ids",
        store=False,
    )
    account_type_ids = fields.Many2many(
        string="Account Types",
        related="general_audit_id.account_type_ids",
        store=False,
    )

    @api.depends(
        "type_id",
    )
    def _compute_allowed_conclusion_ids(self):
        Conclusion = self.env["general_audit_worksheet_conclusion"]
        for record in self:
            result = []
            if record.type_id:
                criteria = [
                    ("type_id", "=", self.type_id.id),
                ]
                result = Conclusion.search(criteria).ids
            record.allowed_conclusion_ids = result

    allowed_conclusion_ids = fields.Many2many(
        string="Allowed Conclusion",
        comodel_name="general_audit_worksheet_conclusion",
        compute="_compute_allowed_conclusion_ids",
        store=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(GeneralAuditWorksheetMixin, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res

    def _compute_policy(self):
        _super = super(GeneralAuditWorksheetMixin, self)
        _super._compute_policy()

    @api.onchange("type_id")
    def onchange_parent_type_id(self):
        self.parent_type_id = self.type_id

    @api.onchange("general_audit_id")
    def onchange_user_id(self):
        self.user_id = self.general_audit_id.user_id

    @api.onchange("general_audit_id")
    def onchange_reviewer_id(self):
        self.reviewer_id = self.general_audit_id.reviewer_id

    def unlink(self):
        worksheets = self.env["general_audit_worksheet"]
        for record in self:
            worksheets += record.worksheet_id
        _super = super(GeneralAuditWorksheetMixin, self)
        _super.unlink()
        worksheets.unlink()

    def write(self, values):
        _super = super(GeneralAuditWorksheetMixin, self)
        _super.write(values)
        for record in self.sudo():
            record._update_parent_worksheet()

    def _update_parent_worksheet(self):
        self.ensure_one()
        self.worksheet_id.write(
            {
                "name": self.name,
                "user_id": self.user_id.id,
                "state": self.state,
                "parent_type_id": self.type_id.id,
            }
        )

    @api.constrains(
        "general_audit_id",
        "type_id",
    )
    def _check_unique_general_audit(self):
        for record in self:
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("type_id", "=", record.type_id.id),
                ("id", "!=", record.id),
            ]
            if not record.type_id.allowed_audit:
                duplicate = self.search(criteria, limit=1)

                if duplicate:
                    error_message = """
                    Context: New data creation for %s
                    Database ID: %s
                    Problem: The selected General Audit is already used in %s.
                    \t\t Each Worksheet must have a unique General Audit.
                    """ % (
                        record.type_id.display_name,
                        record.id,
                        record.display_name,
                    )
                    raise ValidationError(_(error_message))
            else:
                duplicate = self.search(criteria)
                if record.type_id.max_number_allowed >= 1:
                    if len(duplicate) >= record.type_id.max_number_allowed:
                        error_message = """
                        Context: New data creation for %s
                        Database ID: %s
                        Problem: General Audit has exceeded the max. limit allowed
                        \t\t The maximum limit allowed is %s
                        """ % (
                            record.type_id.display_name,
                            record.id,
                            record.type_id.max_number_allowed,
                        )
                        raise ValidationError(_(error_message))

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @ssi_decorator.post_confirm_action()
    def _10_create_preparation_date(self):
        self.ensure_one()
        if not self.preparation_date:
            self.preparation_date = fields.Date.today()

    @ssi_decorator.post_approve_action()
    def _10_create_review_date(self):
        self.ensure_one()
        if not self.review_date:
            self.review_date = fields.Date.today()
