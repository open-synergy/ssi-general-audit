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
        """Create an open worksheet, then its three link siblings.

        The Pre-Condition (an On Progress Final Discussion worksheet whose
        Audit Result, Management Letter, and Management Representation
        siblings only appear/open AFTER the worksheet itself was created)
        is prepared here in Python, so the Links tab starts empty and the
        tour's Reload click has something real to demonstrate -- the
        compute only re-runs when ``general_audit_id`` changes, not when a
        sibling worksheet is created or opened later.
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

        # The de69c2f worksheet is created FIRST, before any sibling
        # exists, so its audit_result_id/management_letter_id/
        # management_representation_id computes all resolve to False at
        # creation time -- see the tour's Post-Condition comment.
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

        # Sibling worksheets the Reload button is expected to find. Opened
        # (not left in draft) -- the compute filters by
        # state in ["open", "done"].
        ws_audit_result = (
            cls.env["general_audit_ws_ff42fdc"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_ff42fdc.id})
        )
        ws_audit_result.with_user(cls.admin).action_open()
        ws_management_letter = (
            cls.env["general_audit_ws_ae598e6"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_ae598e6.id})
        )
        ws_management_letter.with_user(cls.admin).action_open()
        ws_management_representation = (
            cls.env["general_audit_ws_bbbdfe7"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_bbbdfe7.id})
        )
        ws_management_representation.with_user(cls.admin).action_open()

        cls.worksheet.invalidate_cache()

    def test_reload_links(self):
        """Run the Reload Links tour.

        IK: docs/general_audit_ws_de69c2f/02-reload_links.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_de69c2f_reload_links",
            login="admin",
        )
