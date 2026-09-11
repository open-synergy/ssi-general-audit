# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSa025441(YamlTransactionCase):
    """YAML scenario runner for the ``general_audit_ws_a025441`` worksheet."""

    def test_general_audit_ws_a025441(self):
        """Run the a025441 raw_data/conclusion_id/conclusion scenarios."""
        self.run_yaml_scenario("test_data_general_audit_ws_a025441.yaml")
