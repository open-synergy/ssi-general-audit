# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAccountantMenuRelocation(YamlTransactionCase):
    """Test the Accountant menu reorganization (HT/26/000749).

    Covers the ``ir.ui.menu`` data overrides shipped by
    ``ssi_general_audit_core/menu.xml``: the three Configuration
    submenus owned by ``ssi_accountant`` (Services, Financial
    Accounting Standards, Opinions) are reparented under a new
    "Accountant" menu below "Configuration -> Standard & Regulation",
    and the "Accountant" app root menu is hidden from the sidebar for
    every user.
    """

    def test_accountant_menu_relocation(self):
        """Run the Accountant menu relocation YAML scenarios."""
        self.run_yaml_scenario("test_data_accountant_menu_relocation.yaml")
