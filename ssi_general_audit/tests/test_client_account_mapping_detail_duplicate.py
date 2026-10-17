# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAccountMappingDetailDuplicate(YamlTransactionCase):
    """Scenario tests for the duplicate account constraint of a mapping.

    A client account can appear only once in a ``client_account_mapping``;
    a second line for the same account is refused.
    """

    def test_client_account_mapping_detail_duplicate(self):
        """Run the duplicate-account-in-one-mapping scenario."""
        self.run_yaml_scenario("test_data_client_account_mapping_detail_duplicate.yaml")
