# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWorksheetTypeConclusionSource(YamlTransactionCase):
    """Scenario tests for the conclusion source types of a worksheet type."""

    def test_conclusion_source(self):
        """Run the conclusion source type scenarios.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_worksheet_type_conclusion_source.yaml")
