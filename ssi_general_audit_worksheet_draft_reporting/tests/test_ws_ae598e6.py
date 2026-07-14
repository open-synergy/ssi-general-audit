# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSae598e6(YamlTransactionCase):
    def test_ws_ae598e6(self):
        self.run_yaml_scenario("test_data_ws_ae598e6.yaml")
