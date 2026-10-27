# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsF3ed115FillChecklist(HttpSavepointCase):
    """Tour test for the ``general_audit_ws_f3ed115`` Checklist tab."""

    @classmethod
    def setUpClass(cls):
        """Create an Open Final Communication With TCWG worksheet.

        ``user_id`` is explicit: ``cls.env`` runs as SUPERUSER and the
        record rule ``general_audit_ws_f3ed115_internal_user_rule``
        would otherwise hide the fixture from the tour's admin session
        (structure-and-runner.md "Fixture setUpClass berjalan sebagai
        SUPERUSER").
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        cls.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Audit Client - F3ED115 Checklist Tour",
                    "is_company": True,
                }
            )
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - F3ED115 Checklist Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-F3ED115-CHECKLIST-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type Set - F3ED115 Checklist Tour",
                    "code": "/",
                }
            )
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Standard - F3ED115 Checklist Tour",
                    "code": "/",
                }
            )
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - F3ED115 Checklist Tour",
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

        ws_type_f3ed115 = cls.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_f3ed115"
        )
        cls.worksheet = (
            cls.env["general_audit_ws_f3ed115"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_f3ed115.id,
                    "user_id": cls.admin.id,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()
        cls.worksheet.invalidate_cache()

    def test_fill_checklist(self):
        """Run the f3ed115 Fill Review Checklist tour.

        IK: docs/general_audit_ws_f3ed115/01-fill-checklist.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_final_report_f3ed115_fill_checklist",
            login="admin",
        )
