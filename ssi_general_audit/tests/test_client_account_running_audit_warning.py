# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAccountRunningAuditWarning(YamlTransactionCase):
    """Onchange warning of ``client_account`` for a running audit.

    Covers open-synergy/ssi-general-audit#491. Pure Python -- trigger
    P1 (L-01: ``action: form`` and ``call`` do not expose the
    ``warning`` dictionary returned by an onchange method).
    """

    def test_account_can_be_saved(self):
        """Creating an account for a client with a running audit works."""
        self.run_yaml_scenario("test_data_client_account_running_audit_warning.yaml")

    def _create_audit(self, label, partner=None):
        """Create a draft ``general_audit`` for a client.

        :param label: short unique label naming the fixture records
        :param partner: client to audit; a new one is created if empty
        :return: the ``general_audit`` record
        """
        env = self.env
        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        if not partner:
            partner = env["res.partner"].create(
                {"name": "Test Client - %s" % label, "is_company": True}
            )
        accountant = env["res.partner"].create({"name": "Test Accountant - %s" % label})
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-%s" % label.upper().replace(" ", ""),
            }
        )
        account_type_set = env["client_account_type_set"].create(
            {"name": "Type Set - %s" % label, "code": "/"}
        )
        standard = env["accountant.financial_accounting_standard"].create(
            {"name": "Standard - %s" % label, "code": "/"}
        )
        return env["general_audit"].create(
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

    def _warning(self, partner):
        """Return the onchange result for a new account of a client.

        :param partner: client chosen on the new account
        :return: the dictionary returned by the onchange, or ``None``
        """
        account = self.env["client_account"].new({"partner_id": partner.id})
        return account.onchange_partner_running_audit_warning()

    def test_warning_for_open_audit(self):
        """A client with an open audit gets a warning naming the audit.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        audit = self._create_audit("Warn Open")
        audit.action_open()
        result = self._warning(audit.partner_id)
        self.assertTrue(result)
        self.assertEqual(result["warning"]["title"], "Running General Audit")
        self.assertIn(audit.name, result["warning"]["message"])
        self.assertIn("press Account", result["warning"]["message"])

    def test_warning_for_draft_audit(self):
        """A client with a draft audit also gets a warning.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        audit = self._create_audit("Warn Draft")
        result = self._warning(audit.partner_id)
        self.assertTrue(result)
        self.assertIn(audit.name, result["warning"]["message"])

    def test_no_warning_without_audit(self):
        """A client without any audit gets no warning.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        partner = self.env["res.partner"].create(
            {"name": "Test Client - No Audit", "is_company": True}
        )
        self.assertFalse(self._warning(partner))

    def test_no_warning_for_finished_audit(self):
        """A client whose audits are only done or cancelled gets no warning.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        audit = self._create_audit("Warn Done")
        audit.write({"state": "done"})
        other = self._create_audit("Warn Cancel", partner=audit.partner_id)
        other.write({"state": "cancel"})
        self.assertFalse(self._warning(audit.partner_id))

    def test_no_warning_for_existing_account(self):
        """Editing a saved account does not trigger the warning.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        audit = self._create_audit("Warn Existing")
        audit.action_open()
        account = self.env["client_account"].create(
            {
                "name": "Existing Account",
                "code": "9.9.9.91",
                "partner_id": audit.partner_id.id,
            }
        )
        self.assertFalse(account.onchange_partner_running_audit_warning())

    def test_warning_lists_at_most_three_audits(self):
        """More than three running audits are summarised as ``N more``.

        Pure Python -- trigger P1 (L-01: the onchange ``warning`` is lost
        by YAML actions).
        """
        first = self._create_audit("Warn Many 1")
        partner = first.partner_id
        for index in range(2, 6):
            self._create_audit("Warn Many %s" % index, partner=partner)
        result = self._warning(partner)
        self.assertIn("and 2 more", result["warning"]["message"])
