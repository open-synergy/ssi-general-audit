# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditClosing(YamlTransactionCase):
    """Scenario tests for the General Audit closing type and lines."""

    def test_general_audit_closing(self):
        """Run the closing type and closing line scenarios.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_general_audit_closing.yaml")
