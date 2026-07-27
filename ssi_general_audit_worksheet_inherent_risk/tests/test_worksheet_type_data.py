# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWorksheetTypeData(YamlTransactionCase):
    """Test installed data of ``general_audit_worksheet_type`` records.

    Covers the ``standard_item_ids`` field installed by this module for
    the 3 Inherent Risk worksheet types (BFB6DAE, C16ABD7, A418D89).
    """

    def test_worksheet_type_standard_item_ids(self):
        """Assert ``standard_item_ids`` installed data is correct.

        :return: None
        """
        self.run_yaml_scenario("test_data_worksheet_type_standard_item.yaml")
