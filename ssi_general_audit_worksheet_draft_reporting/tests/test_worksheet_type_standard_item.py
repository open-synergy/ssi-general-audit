# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWorksheetTypeStandardItem(YamlTransactionCase):
    def test_worksheet_type_standard_item(self):
        self.run_yaml_scenario("test_worksheet_type_standard_item.yaml")
