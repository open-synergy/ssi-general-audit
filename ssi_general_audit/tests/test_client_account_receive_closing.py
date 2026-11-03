# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAccountReceiveClosing(YamlTransactionCase):
    """Scenario tests for the ``receive_closing`` flag of ``client_account``.

    Only one account of a client can be ticked for each account type.
    """

    def test_client_account_receive_closing(self):
        """Run the unique closing receiver scenario."""
        self.run_yaml_scenario("test_data_client_account_receive_closing.yaml")
