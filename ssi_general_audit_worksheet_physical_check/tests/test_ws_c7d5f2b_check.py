# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWsC7D5F2BCheck(YamlTransactionCase):
    """Scenarios for the ``data_comparison``/``check_line`` child models."""

    def test_ws_c7d5f2b_check(self):
        """Run the data_comparison/check_line YAML scenarios.

        :return: nothing; delegates to ``run_yaml_scenario``.
        """
        self.run_yaml_scenario("test_data_ws_c7d5f2b_check.yaml")
