# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsFf42fdc(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_ff42fdc`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open worksheet with one audited account group.

        The Pre-Condition (an On Progress worksheet linked to an
        engagement whose General Audit has at least one account
        detail line) is prepared here in Python; the tour itself only
        exercises opening the Posture Report tab and clicking Load
        Posture.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule general_audit_ws_ff42fdc_internal_user_rule
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
            .create({"name": "Test Audit Client - FF42FDC Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - FF42FDC Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-FF42FDC-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - FF42FDC Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - FF42FDC Tour", "code": "/"})
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - FF42FDC Tour",
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

        # Unique name asserted by the tour's Post-Condition step, once it
        # shows up as a Posture Report row after Load Posture is clicked.
        account_group = (
            cls.env["client_account_group"]
            .with_user(cls.admin)
            .create({"name": "TOUR-FF42FDC-GROUP", "code": "/", "normal_balance": "dr"})
        )
        account_type = (
            cls.env["client_account_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type - FF42FDC Tour",
                    "code": "/",
                    "group_id": account_group.id,
                    "normal_balance": "dr",
                    # DILARANG membiarkan python_code pada default
                    # "result = document.balance": lihat catatan yang sama
                    # di ssi_general_audit_worksheet_lead_schedule test
                    # data (crash pada extrapolation balance).
                    "python_code": "result = 0.0",
                }
            )
        )
        account = (
            cls.env["client_account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Client Account - FF42FDC Tour",
                    "code": "ACC-FF42FDC-TOUR",
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
        )

        mapping = (
            cls.env["client_account_mapping"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id})
        )
        cls.env["client_account_mapping.detail"].with_user(cls.admin).create(
            {"mapping_id": mapping.id, "account_id": account.id}
        )
        audit.with_user(cls.admin).action_reload_account()

        tb_home = (
            cls.env["client_trial_balance"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "trial_balance_type": "home",
                }
            )
        )
        cls.env["client_trial_balance.detail"].with_user(cls.admin).create(
            {
                "trial_balance_id": tb_home.id,
                "account_id": account.id,
                "debit": 1000000.0,
            }
        )

        ws_type = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_ff42fdc"
        )
        cls.worksheet = (
            cls.env["general_audit_ws_ff42fdc"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type.id,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()
        cls.worksheet.invalidate_cache()

    def test_load_posture(self):
        """Run the Load Posture tour for ``general_audit_ws_ff42fdc``.

        IK: docs/general_audit_ws_ff42fdc/01-load_posture.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_ff42fdc_load_posture",
            login="admin",
        )
