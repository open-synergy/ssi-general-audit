# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAdjustmentEntryDetail(YamlTransactionCase):
    """Scenario tests for the ``client_adjustment_entry.detail`` model.

    Covers the optional ``aje_code`` field added by
    open-synergy/ssi-general-audit#365: a detail line created manually
    (not through the CSV import wizard), without ``aje_code``, must
    save without error since the field is not required.
    """

    def test_client_adjustment_entry_detail(self):
        """Run the ``client_adjustment_entry.detail`` YAML scenarios.

        :return: ``None``
        """
        self.run_yaml_scenario("test_client_adjustment_entry_detail.yaml")
