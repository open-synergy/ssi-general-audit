# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditAdjustmentLink(YamlTransactionCase):
    """Scenario tests for linking adjustment lines to audit details.

    HT/26/000804: ``client_adjustment_entry.detail.detail_id`` stayed
    empty when the ``general_audit.detail`` was created after the line
    or recreated by an account reload, so the adjustment totals of the
    audit detail were 0.
    """

    def test_general_audit_adjustment_link(self):
        """Run the adjustment-line-link-after-reload scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_general_audit_adjustment_link.yaml")
