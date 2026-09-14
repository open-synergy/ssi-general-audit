# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestImportAdjustmentEntryDetail(YamlTransactionCase):
    """Scenario tests for the ``import_adjustment_entry_detail`` wizard.

    Covers the CSV import button added to the ``client_adjustment_entry``
    "Details" page (open-synergy/ssi-general-audit#339): a valid CSV
    creates new detail lines, an unknown account code raises
    ``UserError`` without creating any line.
    """

    def _create_adjustment_entry(self):
        """Build a draft ``client_adjustment_entry`` with two accounts.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field must hold a base64-encoded CSV file, and ``EVAL:`` has no
        ``base64``/``import`` available to build that value in YAML).

        :return: tuple ``(entry, known_account)`` -- the draft entry and
            one ``client_account`` known to its client partner
        """
        client = self.env["res.partner"].create(
            {
                "name": "Test Client - Import Adjustment Entry",
                "is_company": True,
            }
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Accountant - Import Adjustment Entry"}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-IMPORT-ADJ-0001",
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test Account Type Set - Import Adjustment", "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {
                "name": "Test Financial Accounting Standard - Import Adj",
                "code": "/",
            }
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Test General Audit - Import Adjustment Entry",
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
                "name": "Test Group - Import Adjustment",
                "code": "/",
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        account_type = self.env["client_account_type"].create(
            {
                "name": "Cash - Import Adjustment",
                "code": "/",
                "group_id": group.id,
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        known_account = self.env["client_account"].create(
            {
                "name": "Kas Test - Import Adjustment",
                "code": "KASIMPORTADJ",
                "partner_id": client.id,
                "type_id": account_type.id,
            }
        )
        entry = self.env["client_adjustment_entry"].create(
            {
                "general_audit_id": audit.id,
                "adjustment_type": "propose",
            }
        )
        return entry, known_account

    def test_import_valid_csv_creates_detail_lines(self):
        """A CSV with two known account codes creates two detail lines.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        entry, known_account = self._create_adjustment_entry()
        csv_content = (
            "%s,Cash adjustment,100.0,0.0\n" "%s,Reversal of cash adjustment,0.0,40.0\n"
        ) % (known_account.code, known_account.code)
        wizard = self.env["import_adjustment_entry_detail"].create(
            {
                "entry_id": entry.id,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )
        wizard.button_import()
        self.assertEqual(len(entry.detail_ids), 2)
        first, second = entry.detail_ids[0], entry.detail_ids[1]
        self.assertEqual(first.account_id, known_account)
        self.assertEqual(first.name, "Cash adjustment")
        self.assertEqual(first.debit, 100.0)
        self.assertEqual(first.credit, 0.0)
        self.assertEqual(second.account_id, known_account)
        self.assertEqual(second.name, "Reversal of cash adjustment")
        self.assertEqual(second.debit, 0.0)
        self.assertEqual(second.credit, 40.0)

    def test_import_unknown_account_code_raises_and_creates_nothing(self):
        """An unknown account code raises ``UserError``, no line created.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        entry, _known_account = self._create_adjustment_entry()
        csv_content = "DOES-NOT-EXIST,Unmapped line,10.0,0.0\n"
        wizard = self.env["import_adjustment_entry_detail"].create(
            {
                "entry_id": entry.id,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )
        with self.assertRaises(UserError):
            wizard.button_import()
        self.assertEqual(len(entry.detail_ids), 0)
