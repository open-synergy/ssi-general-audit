# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAdjustingCoaNegative(YamlTransactionCase):
    """Negative tests for ``client_adjusting_coa`` on confirm."""

    def test_client_adjusting_coa_negative(self):
        """Run the confirm scenario: invalid lines are rejected."""
        self.run_yaml_scenario("test_data_adjusting_coa_negative.yaml")
