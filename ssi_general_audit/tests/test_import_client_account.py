# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestImportClientAccount(YamlTransactionCase):
    """Scenario tests for the ``import_client_account`` wizard.

    Covers the row validation and preview added by
    open-synergy/ssi-general-audit#393: a header row and rows with an
    empty or over-length code are skipped instead of being created, a
    new account whose name collides with another active account of the
    same partner is still created but flagged in the closing
    notification, and neither case blocks the import.
    """

    def _create_mapping(self, label):
        """Build a draft ``client_account_mapping`` for a fresh client.

        Pure Python -- trigger P10 (L-09..L-11: the fixture needs a
        ``general_audit`` opened through several dependent master data
        records, which is impractical to build in one ``EVAL:``
        expression).

        :param label: short unique label used to name every fixture
            record created, so parallel test methods do not collide
        :return: tuple ``(mapping, partner)`` -- the draft
            ``client_account_mapping`` and its client ``res.partner``
        """
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        partner = self.env["res.partner"].create(
            {"name": "Test Client - %s" % label, "is_company": True}
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Accountant - %s" % label}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-%s" % label.upper().replace(" ", ""),
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Type Set - %s" % label, "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {"name": "Standard - %s" % label, "code": "/"}
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Audit - %s" % label,
                "partner_id": partner.id,
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
        mapping = self.env["client_account_mapping"].create(
            {"general_audit_id": audit.id}
        )
        return mapping, partner

    def test_import_with_header_skips_first_row(self):
        """Two valid rows import after the header row is skipped.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        mapping, partner = self._create_mapping("Import CSV Header")
        csv_content = "Code,Name,Extra,TypeCode\n" "ACC-001,Cash,,\n" "ACC-002,Bank,,\n"
        wizard = self.env["import_client_account"].create(
            {
                "mapping_id": mapping.id,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )
        result = wizard.button_import()
        accounts = self.env["client_account"].search([("partner_id", "=", partner.id)])
        self.assertEqual(len(accounts), 2)
        self.assertEqual(
            result["params"]["message"], "2 imported, 0 updated, 0 skipped."
        )

    def test_import_skips_empty_and_overlength_code_rows(self):
        """Rows with an empty or over-length code are skipped, not created.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        mapping, partner = self._create_mapping("Import CSV Skip")
        long_code = "A" * 40
        csv_content = (
            ",Should Skip Empty Code,,\n" "%s,Should Skip Long Code,,\n"
        ) % long_code
        wizard = self.env["import_client_account"].create(
            {
                "mapping_id": mapping.id,
                "has_header": False,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )
        result = wizard.button_import()
        accounts = self.env["client_account"].search([("partner_id", "=", partner.id)])
        self.assertEqual(len(accounts), 0)
        self.assertEqual(
            result["params"]["message"], "0 imported, 0 updated, 2 skipped."
        )

    def test_import_duplicate_name_created_but_warned(self):
        """A new account with a colliding name is created, not blocked.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        mapping, partner = self._create_mapping("Import CSV Dup Name")
        self.env["client_account"].create(
            {
                "code": "ACC-100",
                "name": "Cash",
                "partner_id": partner.id,
            }
        )
        csv_content = "ACC-200,Cash,,\n"
        wizard = self.env["import_client_account"].create(
            {
                "mapping_id": mapping.id,
                "has_header": False,
                "data": base64.b64encode(csv_content.encode("utf-8")),
            }
        )
        result = wizard.button_import()
        new_account = self.env["client_account"].search(
            [("partner_id", "=", partner.id), ("code", "=", "ACC-200")]
        )
        self.assertEqual(len(new_account), 1)
        self.assertEqual(new_account.name, "Cash")
        self.assertIn(
            "Duplicate name warning for: ACC-200/Cash",
            result["params"]["message"],
        )

    def _create_two_types(self, label):
        """Create two account types usable as CSV type codes.

        Pure Python -- trigger P10 (L-09..L-11: the fixture needs a
        group plus types whose explicit unique codes feed the CSV).

        The code stays unique on purpose: the wizard looks a type up by
        code, and the placeholder ``"/"`` is never generated on create.

        :param label: short unique label used to name the records
        :return: tuple ``(type_a, type_b)`` of ``client_account_type``
        """
        group = self.env["client_account_group"].create(
            {
                "name": "Group - %s" % label,
                "code": "/",
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        types = self.env["client_account_type"]
        for suffix in ("A", "B"):
            types |= self.env["client_account_type"].create(
                {
                    "name": "Type %s - %s" % (suffix, label),
                    "code": "T%s-%s" % (suffix, label.replace(" ", "")),
                    "group_id": group.id,
                    "sequence": 1,
                    "normal_balance": "dr",
                    "python_code": "result = 0.0",
                }
            )
        return types[0], types[1]

    def _run_type_import(self, label, **wizard_vals):
        """Import a CSV over an existing type-A account.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).

        :param label: short unique label used to name the fixtures
        :param wizard_vals: extra values for the wizard, such as
            ``keep_existing_type``
        :return: tuple ``(mapping, partner, type_a, type_b)``
        """
        mapping, partner = self._create_mapping(label)
        type_a, type_b = self._create_two_types(label)
        self.env["client_account"].create(
            {
                "code": "ACC-EX",
                "name": "Existing",
                "partner_id": partner.id,
                "type_id": type_a.id,
            }
        )
        csv_content = "ACC-EX,Existing,,%s\nACC-NEW,Brand New,,%s\n" % (
            type_b.code,
            type_b.code,
        )
        vals = {
            "mapping_id": mapping.id,
            "has_header": False,
            "data": base64.b64encode(csv_content.encode("utf-8")),
        }
        vals.update(wizard_vals)
        wizard = self.env["import_client_account"].create(vals)
        self.assertEqual(
            wizard.keep_existing_type, vals.get("keep_existing_type", True)
        )
        wizard.button_import()
        return mapping, partner, type_a, type_b

    def _get_account(self, partner, code):
        """Return the ``client_account`` of ``partner`` with ``code``.

        Pure Python -- trigger P10 (L-09..L-11: shared lookup helper
        for the Python-only fixtures in this class).

        :param partner: client ``res.partner``
        :param code: account code to look up
        :return: matching ``client_account`` recordset
        """
        return self.env["client_account"].search(
            [("partner_id", "=", partner.id), ("code", "=", code)]
        )

    def test_keep_existing_type_default_keeps_type(self):
        """By default an existing account keeps its type.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        mapping, partner, type_a, type_b = self._run_type_import("Keep Default")
        existing = self._get_account(partner, "ACC-EX")
        self.assertEqual(existing.type_id, type_a)
        self.assertEqual(self._get_account(partner, "ACC-NEW").type_id, type_b)
        details = self.env["client_account_mapping.detail"].search(
            [("mapping_id", "=", mapping.id), ("account_id", "=", existing.id)]
        )
        self.assertEqual(len(details), 1)

    def test_keep_existing_type_false_overwrites_type(self):
        """With the flag off the CSV type overwrites; no duplicate rows.

        Pure Python -- trigger P10 (L-09..L-11: the wizard's ``data``
        field needs a base64-encoded CSV fixture, unavailable in
        ``EVAL:``).
        """
        mapping, partner, type_a, type_b = self._run_type_import(
            "Keep Off", keep_existing_type=False
        )
        existing = self._get_account(partner, "ACC-EX")
        self.assertEqual(existing.type_id, type_b)
        wizard = self.env["import_client_account"].create(
            {
                "mapping_id": mapping.id,
                "has_header": False,
                "keep_existing_type": False,
                "data": base64.b64encode(
                    ("ACC-EX,Existing,,%s\n" % type_b.code).encode("utf-8")
                ),
            }
        )
        wizard.button_import()
        details = self.env["client_account_mapping.detail"].search(
            [("mapping_id", "=", mapping.id), ("account_id", "=", existing.id)]
        )
        self.assertEqual(len(details), 1)
