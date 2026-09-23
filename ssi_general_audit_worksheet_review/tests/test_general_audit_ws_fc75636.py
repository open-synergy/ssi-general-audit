# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSfc75636(YamlTransactionCase):
    """YAML scenario runner for the ``general_audit_ws_fc75636`` worksheet."""

    def test_general_audit_ws_fc75636(self):
        """Run the fc75636 Links tab (Reload), Draft Audit Opinion, and
        b66777d Populate Final Audit Opinion scenarios.
        """
        self.run_yaml_scenario("test_data_general_audit_ws_fc75636.yaml")
