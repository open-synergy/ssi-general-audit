# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiClientAdjustmentEntry(HttpSavepointCase):
    """Tour tests for the ``client_adjustment_entry`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit and a Draft Adjusting Journal.

        The Pre-Condition of the import tour is prepared here in Python:
        an On Progress General Audit for a client named ``Test Audit
        Client - Adjustment Entry Tour`` and one Adjusting Journal in
        Draft.
        """
        super().setUpClass()
        # user_id is explicit: cls.env runs as SUPERUSER, and the record
        # rule adjustment_entry_internal_user_rule would otherwise hide
        # the fixture from the tour's admin session.
        cls.admin = cls.env.ref("base.user_admin")
        env = cls.env

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = (
            env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Audit Client - Adjustment Entry Tour",
                    "is_company": True,
                }
            )
        )
        accountant = (
            env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - Adjustment Entry Tour"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-AJE-TOUR-0001",
            }
        )
        type_set = (
            env["client_account_type_set"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type Set - Adjustment Entry Tour",
                    "code": "/",
                }
            )
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - Adjustment Entry Tour", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - Adjustment Entry Tour",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": type_set.id,
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
        cls.entry = (
            env["client_adjustment_entry"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "adjustment_type": "propose",
                    "user_id": cls.admin.id,
                }
            )
        )

    def test_import(self):
        """Run the import tour for ``client_adjustment_entry``.

        IK: docs/client_adjustment_entry/01-import.md

        The tour stops at the Import dialog and closes it with Cancel: a
        file upload has no DOM completion signal. The imported lines are
        covered by ``test_import_adjustment_entry_detail``.
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_client_adjustment_entry_import",
            login="admin",
        )
