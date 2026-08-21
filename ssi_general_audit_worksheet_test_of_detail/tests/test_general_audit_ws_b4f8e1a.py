# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSB4f8e1a(YamlTransactionCase):
    """Cover CRUD and the base workflow for ``general_audit_ws_b4f8e1a``."""

    def test_general_audit_ws_b4f8e1a(self):
        """Run the YAML scenario covering this worksheet."""
        self.run_yaml_scenario("test_data_general_audit_ws_b4f8e1a.yaml")
