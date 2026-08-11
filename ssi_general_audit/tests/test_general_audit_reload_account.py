# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

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
