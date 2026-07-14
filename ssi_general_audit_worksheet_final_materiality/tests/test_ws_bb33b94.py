# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSBb33b94(YamlTransactionCase):
    def test_ws_bb33b94(self):
        self.run_yaml_scenario("test_data_ws_bb33b94.yaml")
