# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditAuditFee(YamlTransactionCase):
    """Scenario tests for the Audit Fee field and the Note page order."""

    def test_audit_fee(self):
        """Run the stored value and zero default scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_general_audit_audit_fee.yaml")

    def test_note_page_after_policy(self):
        """Assert the Note page comes after the Policies page.

        Pure Python -- trigger P12 (L-20: the page order exists only in
        the combined form view, which a YAML step cannot inspect).

        :return: ``None``
        """
        arch = self.env["general_audit"].fields_view_get(view_type="form")["arch"]
        root = etree.fromstring(arch)
        names = [p.get("name") for p in root.iter("page")]
        self.assertIn("other", names)
        self.assertGreater(names.index("note"), names.index("policy"))
