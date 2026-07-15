# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSChecklist(YamlTransactionCase):
    """Covers be62e79, dae9f3c, fc75636 and the fc75636.category master."""

    def test_general_audit_ws_checklist(self):
        self.run_yaml_scenario("test_data_general_audit_ws_checklist.yaml")
