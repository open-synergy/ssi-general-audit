# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSa8c54f3Links(YamlTransactionCase):
    """Scenario tests for ``link_42_id``..``link_47_id`` on
    ``general_audit_ws_a8c54f3``, added by this module's extension."""

    def test_general_audit_ws_a8c54f3_links(self):
        """Run the link_42..link_47 compute/negative-path YAML scenarios."""
        self.run_yaml_scenario("test_data_general_audit_ws_a8c54f3_links.yaml")
