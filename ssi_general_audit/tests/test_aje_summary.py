# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAjeSummary(YamlTransactionCase):
    """Scenario tests for the AJE Summaries page of the general audit.

    HT/26/000811: the page lists the lines of the done adjustment entries
    with their impact on the financial statement categories.
    """

    def test_aje_summary(self):
        """Run the impact columns and summary lines scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_aje_summary.yaml")
