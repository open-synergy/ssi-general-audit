# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWorksheetTypeStandardItem(YamlTransactionCase):
    """Test installed ``standard_item_ids`` data on worksheet types shipped
    by this module."""

    def test_general_audit_worksheet_type_standard_item(self):
        """Run the standard_item_ids installed-data scenario."""
        self.run_yaml_scenario("test_data_worksheet_type_standard_item.yaml")
