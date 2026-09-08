# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsDe69c2f(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_de69c2f`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open worksheet with one sibling of each kind.

        The Pre-Condition (an On Progress Final Discussion worksheet
        linked to an engagement that already has an Audit Result,
        Management Letter, and Management Representation worksheet) is
        prepared here in Python; each tour only exercises opening the
        relevant tab and clicking its Reload button.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule general_audit_ws_de69c2f_internal_user_rule
        # would otherwise hide these fixtures from the tour's admin
        # session (structure-and-runner.md "Fixture setUpClass berjalan
        # sebagai SUPERUSER").
        cls.admin = cls.env.ref("base.user_admin")

        cls.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Client - DE69C2F Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - DE69C2F Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-DE69C2F-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - DE69C2F Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - DE69C2F Tour", "code": "/"})
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - DE69C2F Tour",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": account_type_set.id,
                    "financial_accounting_standard_id": standard.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        audit.with_user(cls.admin).action_open()

        ws_type_de69c2f = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_de69c2f"
        )
        ws_type_ff42fdc = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_ff42fdc"
        )
        ws_type_ae598e6 = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_ae598e6"
        )
        ws_type_bbbdfe7 = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_bbbdfe7"
        )

        # Sibling worksheets the three Reload buttons are expected to
        # find. Left in "draft" -- the reload searches by
        # general_audit_id only, not by state.
        cls.env["general_audit_ws_ff42fdc"].with_user(cls.admin).create(
            {"general_audit_id": audit.id, "type_id": ws_type_ff42fdc.id}
        )
        cls.env["general_audit_ws_ae598e6"].with_user(cls.admin).create(
            {"general_audit_id": audit.id, "type_id": ws_type_ae598e6.id}
        )
        cls.env["general_audit_ws_bbbdfe7"].with_user(cls.admin).create(
            {"general_audit_id": audit.id, "type_id": ws_type_bbbdfe7.id}
        )

        cls.worksheet = (
            cls.env["general_audit_ws_de69c2f"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_de69c2f.id,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()
        cls.worksheet.invalidate_cache()

    def test_reload_audit_result(self):
        """Run the Reload Audit Result tour.

        IK: docs/general_audit_ws_de69c2f/02-reload_audit_result.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_audit_result",
            login="admin",
        )

    def test_reload_management_letter(self):
        """Run the Reload Management Letter tour.

        IK: docs/general_audit_ws_de69c2f/03-reload_management_letter.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting"
            "_de69c2f_reload_management_letter",
            login="admin",
        )

    def test_reload_management_representation(self):
        """Run the Reload Management Representation tour.

        IK: docs/general_audit_ws_de69c2f/04-reload_management_representation.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting"
            "_de69c2f_reload_management_representation",
            login="admin",
        )
