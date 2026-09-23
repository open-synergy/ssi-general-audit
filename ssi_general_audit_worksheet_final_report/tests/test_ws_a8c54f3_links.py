# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSa8c54f3Links(YamlTransactionCase):
    """Scenario tests for the ``general_audit_ws_a8c54f3`` Link fields."""

    def test_ws_a8c54f3_links(self):
        """Run the Link field compute/reload YAML scenarios."""
        self.run_yaml_scenario("test_data_ws_a8c54f3_links.yaml")
