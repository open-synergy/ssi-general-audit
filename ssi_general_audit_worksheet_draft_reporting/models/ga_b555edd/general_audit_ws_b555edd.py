# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSb555edd(models.Model):
    """Worksheet — Report Formatting Control (b555edd).

    A quality-control worksheet for reviewing the formatting, grammar,
    consistency, and presentation quality of the draft auditor's report
    before partner sign-off and issuance.  Ensures the report meets the
    firm's style and quality standards.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 700/SA 700 (Forming an Opinion and Reporting).
    """

    _name = "general_audit_ws_b555edd"
    _description = "Report Formatting Control (b555edd)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_b555edd"
    )

    #: ``client_account_group.code`` values shown on the Statement of
    #: Financial Position tab (T001-T008) and on the Statement of
    #: Comprehensive Income tab (T009-T015).
    _SFP_GROUP_CODES = [f"T{number:03d}" for number in range(1, 9)]
    _SOCI_GROUP_CODES = [f"T{number:03d}" for number in range(9, 16)]

    detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Details",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
        },
        help="One line per standard account type of the General Audit.",
    )
    sfp_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Statement of Financial Position",
        domain=[("group_id.code", "in", _SFP_GROUP_CODES)],
        readonly=True,
        help=(
            "Detail lines whose account group is T001-T008 "
            "(assets, liabilities and equity)."
        ),
    )
    soci_detail_ids = fields.One2many(
        comodel_name="general_audit_ws_b555edd.detail",
        inverse_name="worksheet_id",
        string="Statement of Comprehensive Income",
        domain=[("group_id.code", "in", _SOCI_GROUP_CODES)],
        readonly=True,
        help=(
            "Detail lines whose account group is T009-T015 "
            "(revenue, expenses and other comprehensive income)."
        ),
    )

    def action_reload_account(self):
        """Refill the detail lines from the General Audit standard details.

        :return: None
        """
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        """Replace the detail lines with one line per standard detail.

        Every standard account type of the General Audit gets a line,
        whether it belongs to the financial position or to the
        comprehensive income statement. Existing lines are removed
        first, so clicking Reload again never duplicates lines.

        :return: None
        """
        self.ensure_one()
        self.detail_ids.unlink()
        Detail = self.env["general_audit_ws_b555edd.detail"]
        for standard_detail in self.general_audit_id.standard_detail_ids:
            type_ = standard_detail.type_id
            Detail.create(
                {
                    "worksheet_id": self.id,
                    "standard_detail_id": standard_detail.id,
                    "sequence": type_.group_id.sequence * 1000 + type_.sequence,
                }
            )
