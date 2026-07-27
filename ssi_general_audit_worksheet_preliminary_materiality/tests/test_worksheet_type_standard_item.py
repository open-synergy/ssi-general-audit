# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWorksheetTypeStandardItem(YamlTransactionCase):
    def test_worksheet_type_standard_item_ids(self):
        """Verify ``standard_item_ids`` installed data (issue #198) for the
        3 ``general_audit_worksheet_type`` records defined by this module.
        """
        self.run_yaml_scenario("test_data_worksheet_type_standard_item.yaml")
