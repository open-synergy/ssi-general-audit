# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAddClientAccount(YamlTransactionCase):
    """Scenario tests for the ``add_client_account`` wizard.

    Covers open-synergy/ssi-general-audit#489: valid lines create
    client accounts and mapping rows together, a same-name account is
    created but warned, and any invalid line aborts the whole action
    without creating an account.
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

    def _create_wizard(self, mapping, lines):
        """Build the wizard with the given account lines.

        Pure Python -- trigger P10 (L-09..L-11: the lines are built
        from a data-driven list, unavailable in ``EVAL:``).

        :param mapping: ``client_account_mapping`` the wizard opens on
        :param lines: list of ``(code, name)`` tuples
        :return: the ``add_client_account`` record
        """
        account_type = self.env["client_account_type"].search([], limit=1)
        return self.env["add_client_account"].create(
            {
                "mapping_id": mapping.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {"code": code, "name": name, "type_id": account_type.id},
                    )
                    for code, name in lines
                ],
            }
        )

    def _assert_rejected(self, label, lines, expected):
        """Run the wizard and check nothing is created.

        Pure Python -- trigger P1 (L-01: ``expect_error`` cannot
        compare the account count before and after the failure).

        :param label: unique label of the fixture
        :param lines: list of ``(code, name)`` tuples
        :param expected: text the error message must contain
        """
        mapping, partner = self._create_mapping(label)
        self.env["client_account"].create(
            {"code": "EXIST-1", "name": "Existing", "partner_id": partner.id}
        )
        domain = [("partner_id", "=", partner.id)]
        before = self.env["client_account"].search_count(domain)
        wizard = self._create_wizard(mapping, lines)
        with self.assertRaises(UserError) as ctx:
            wizard.action_add()
        self.assertIn(expected, ctx.exception.args[0])
        self.assertEqual(self.env["client_account"].search_count(domain), before)
        self.assertFalse(mapping.detail_ids)

    def test_add_valid_lines(self):
        """Two valid lines create two accounts and two mapping rows.

        Pure Python -- trigger P10 (L-09..L-11: needs the mapping
        fixture built by ``_create_mapping``).
        """
        mapping, partner = self._create_mapping("Add Valid")
        wizard = self._create_wizard(mapping, [("N-1", "Cash"), ("N-2", "Bank")])
        self.assertEqual(wizard.partner_id, partner)
        result = wizard.action_add()
        accounts = self.env["client_account"].search([("partner_id", "=", partner.id)])
        self.assertEqual(sorted(accounts.mapped("code")), ["N-1", "N-2"])
        self.assertEqual(len(mapping.detail_ids), 2)
        self.assertEqual(mapping.detail_ids.mapped("account_id"), accounts)
        self.assertEqual(result["params"]["type"], "success")
        self.assertEqual(
            result["params"]["next"], {"type": "ir.actions.act_window_close"}
        )

    def test_add_same_name_is_warned(self):
        """A colliding name is created and flagged in the notification.

        Pure Python -- trigger P10 (L-09..L-11: needs the mapping
        fixture built by ``_create_mapping``).
        """
        mapping, partner = self._create_mapping("Add Same Name")
        self.env["client_account"].create(
            {"code": "OLD-1", "name": "Cash", "partner_id": partner.id}
        )
        wizard = self._create_wizard(mapping, [("NEW-1", "cash")])
        result = wizard.action_add()
        created = self.env["client_account"].search(
            [("partner_id", "=", partner.id), ("code", "=", "NEW-1")]
        )
        self.assertEqual(len(created), 1)
        self.assertEqual(len(mapping.detail_ids), 1)
        self.assertIn(
            "Duplicate name warning for: NEW-1/cash", result["params"]["message"]
        )

    def test_add_existing_code_rejected(self):
        """A code already used by the client aborts everything.

        Pure Python -- trigger P1 (L-01), see ``_assert_rejected``.
        """
        self._assert_rejected(
            "Add Existing", [("OK-1", "Fine"), ("EXIST-1", "Dup")], "EXIST-1"
        )

    def test_add_duplicate_code_in_wizard_rejected(self):
        """The same code twice inside the wizard aborts everything.

        Pure Python -- trigger P1 (L-01), see ``_assert_rejected``.
        """
        self._assert_rejected(
            "Add Twice", [("TW-1", "One"), ("TW-1", "Two")], "TW-1 is used twice"
        )

    def test_add_empty_code_rejected(self):
        """An empty code aborts everything.

        Pure Python -- trigger P1 (L-01), see ``_assert_rejected``.
        """
        self._assert_rejected("Add Empty", [("  ", "No Code")], "Empty code")

    def test_add_overlength_code_rejected(self):
        """A 33-character code aborts everything.

        Pure Python -- trigger P1 (L-01), see ``_assert_rejected``.
        """
        self._assert_rejected(
            "Add Long", [("A" * 33, "Too Long")], "longer than 32 characters"
        )

    def test_add_without_lines_rejected(self):
        """A wizard with no line is refused.

        Pure Python -- trigger P1 (L-01), see ``_assert_rejected``.
        """
        self._assert_rejected("Add Empty Wizard", [], "No account line")
