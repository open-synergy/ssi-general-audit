# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestImportTrialBalanceDetail(YamlTransactionCase):
    """Scenario tests for the ``import_trial_balance_detail`` wizard.

    Covers the header option and the import preview added by
    open-synergy/ssi-general-audit#530: with ``has_header`` unset every
    row updates the matching detail, with it set the first row is
    ignored, and the preview counts processed and skipped rows
    (unknown account codes are skipped, as before).
    """

    def _create_trial_balance(self):
        """Build a draft trial balance with two detail lines.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field must hold a base64-encoded CSV file, and ``EVAL:`` has no
        ``base64``/``import`` available to build that value in YAML).

        :return: tuple ``(trial_balance, detail_a, detail_b)`` -- the
            trial balance and its two detail lines (codes ``TBIMP-A``
            and ``TBIMP-B``)
        """
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = self.env["res.partner"].create(
            {"name": "Test Client - Import Trial Balance", "is_company": True}
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Accountant - Import Trial Balance"}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-IMPORT-TB-0001",
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test Type Set - Import Trial Balance", "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {"name": "Test Standard - Import Trial Balance", "code": "/"}
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Test General Audit - Import Trial Balance",
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
        audit.action_open()
        group = self.env["client_account_group"].create(
            {
                "name": "Test Group - Import Trial Balance",
                "code": "/",
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        account_type = self.env["client_account_type"].create(
            {
                "name": "Cash - Import Trial Balance",
                "code": "/",
                "group_id": group.id,
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        trial_balance = self.env["client_trial_balance"].create(
            {"general_audit_id": audit.id, "trial_balance_type": "home"}
        )
        details = self.env["client_trial_balance.detail"]
        for code in ("TBIMP-A", "TBIMP-B"):
            account = self.env["client_account"].create(
                {
                    "name": "Account %s" % code,
                    "code": code,
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
            details |= self.env["client_trial_balance.detail"].create(
                {"trial_balance_id": trial_balance.id, "account_id": account.id}
            )
        return trial_balance, details[0], details[1]

    def _create_wizard(self, trial_balance, csv_content, has_header):
        """Create the import wizard for a trial balance and CSV text.

        :param trial_balance: target ``client_trial_balance``
        :param csv_content: CSV file content as text
        :param has_header: value of the ``has_header`` option
        :return: the ``import_trial_balance_detail`` record
        """
        return self.env["import_trial_balance_detail"].create(
            {
                "trial_balance_id": trial_balance.id,
                "has_header": has_header,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )

    def test_has_header_defaults(self):
        """Trial Balance and Adjustment Entry wizards both default to header.

        Pure Python -- trigger P10 (L-09..L-11: reads wizard defaults
        through ``default_get``, which ``EVAL:`` cannot call with the
        field list needed here).
        """
        trial_balance_wizard = self.env["import_trial_balance_detail"]
        adjustment_wizard = self.env["import_adjustment_entry_detail"]
        self.assertTrue(trial_balance_wizard.default_get(["has_header"])["has_header"])
        self.assertTrue(adjustment_wizard.default_get(["has_header"])["has_header"])

    def test_import_without_header_updates_all_rows(self):
        """Without header, every row writes values to its detail.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        trial_balance, detail_a, detail_b = self._create_trial_balance()
        csv_content = "TBIMP-A,Cash,10,0,100,0\nTBIMP-B,Bank,0,20,0,50\n"
        self._create_wizard(trial_balance, csv_content, False).button_import()
        self.assertEqual(detail_a.opening_balance_debit, 10.0)
        self.assertEqual(detail_a.debit, 100.0)
        self.assertEqual(detail_b.opening_balance_credit, 20.0)
        self.assertEqual(detail_b.credit, 50.0)

    def test_import_with_header_skips_first_row(self):
        """With header, the first row changes no detail.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        trial_balance, detail_a, detail_b = self._create_trial_balance()
        csv_content = "TBIMP-A,Cash,10,0,100,0\nTBIMP-B,Bank,0,20,0,50\n"
        self._create_wizard(trial_balance, csv_content, True).button_import()
        self.assertEqual(detail_a.debit, 0.0)
        self.assertEqual(detail_a.opening_balance_debit, 0.0)
        self.assertEqual(detail_b.credit, 50.0)

    def test_preview_counts_processed_and_skipped_rows(self):
        """Preview counts known rows and skips header and unknown codes.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        trial_balance, _detail_a, _detail_b = self._create_trial_balance()
        csv_content = (
            "Code,Name,OD,OC,D,C\n"
            "TBIMP-A,Cash,10,0,100,0\n"
            "TBIMP-B,Bank,0,20,0,50\n"
            "UNKNOWN,Other,0,0,1,1\n"
        )
        wizard = self._create_wizard(trial_balance, csv_content, False)
        wizard.onchange_import_summary()
        self.assertIn("Rows to be processed: 2", wizard.import_summary)
        self.assertIn("Rows to be skipped: 2", wizard.import_summary)
        self.assertIn("Test Client - Import Trial Balance", wizard.import_summary)
        wizard.has_header = True
        wizard.onchange_import_summary()
        self.assertIn("Rows to be processed: 2", wizard.import_summary)
        self.assertIn("Rows to be skipped: 2", wizard.import_summary)
