# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditReloadAccount(YamlTransactionCase):
    """Scenario tests for ``general_audit._reload_account``.

    HT/26/000648: approving a Client Account Mapping (``CAM/xxx``) calls
    ``general_audit.action_reload_account()``, which used to unlink all
    ``general_audit.detail`` records unconditionally. Once a Lead
    Schedule - Account worksheet (``general_audit_ws_f9f3299``) already
    has detail lines pointing at those records via a required,
    on-delete-restrict FK, the unlink fails with a database constraint
    error and the approval is blocked.
    """

    def test_general_audit_reload_account(self):
        """Run the dependent-worksheet-survives-reload scenario."""
        self.run_yaml_scenario("test_data_general_audit_reload_account.yaml")

    def test_general_audit_reload_account_diff(self):
        """Run the difference-based reload scenario.

        Covers added and removed accounts, kept details, idempotency,
        the blocks for an adjustment entry and the last account of a
        type, and an audit without account mapping.
        """
        self.run_yaml_scenario("test_data_general_audit_reload_account_diff.yaml")

    def test_restrict_pair_with_missing_field_is_skipped(self):
        """Skip restrict pairs whose field does not exist.

        Pure Python -- trigger P6 (L-15..L-18: the class attribute
        ``_reload_account_restrict_models`` must be patched for the
        duration of the test). Covers open-synergy/ssi-general-audit#517.
        """
        model = self.env["general_audit"]
        pairs = [
            ("general_audit.detail", "no_such_field_id"),
            ("no.such.model", "detail_id"),
        ]
        audit = model.new({})
        empty = self.env["client_account"]
        with mock.patch.object(type(model), "_reload_account_restrict_models", pairs):
            self.assertEqual(audit._get_restrict_pairs(), [])
            self.assertTrue(audit._check_accounts_removable(empty, empty))
            self.assertTrue(audit._remove_accounts(empty))
