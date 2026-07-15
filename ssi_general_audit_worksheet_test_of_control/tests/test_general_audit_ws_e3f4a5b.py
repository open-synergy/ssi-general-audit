# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSe3f4a5b(YamlTransactionCase):
    def test_general_audit_ws_e3f4a5b(self):
        self.run_yaml_scenario("test_data_general_audit_ws_e3f4a5b.yaml")
