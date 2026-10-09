# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCorrectedAdjustment(YamlTransactionCase):
    """Scenario tests for the ``corrected`` flag of adjustment entries.

    HT/26/000811: adjustment entries that the client did not correct must
    not be counted in the Adjustment figures of the audit worksheets.
    """

    def test_corrected_adjustment(self):
        """Run the corrected-versus-uncorrected adjustment scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_corrected_adjustment.yaml")
