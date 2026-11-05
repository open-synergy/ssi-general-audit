# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClosingRecompute(YamlTransactionCase):
    """Scenario tests for the automatic closing lines regeneration."""

    def test_closing_recompute(self):
        """Run the closing regeneration scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_closing_recompute.yaml")
