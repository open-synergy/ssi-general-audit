# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSa58e29c(YamlTransactionCase):
    def test_ws_a58e29c(self):
        self.run_yaml_scenario("test_data_ws_a58e29c.yaml")
