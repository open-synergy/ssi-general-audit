# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSc3b9e71(YamlTransactionCase):
    """Scenario tests for the Uncorrected AJE Analysis worksheet.

    HT/26/000811: the worksheet compares the uncorrected adjustment entries
    with the audited balance of each account group and with Performance
    Materiality.
    """

    def test_general_audit_ws_c3b9e71(self):
        """Run the uncorrected AJE analysis scenario.

        :return: ``None``
        """
        self.run_yaml_scenario("test_data_general_audit_ws_c3b9e71.yaml")

    def test_default_adjustment_entry_views_stay_editable(self):
        """Assert the read-only AJE views are not the default views.

        Pure Python, trigger P1 and limitation L-01: the ``call`` action
        discards the return value of ``fields_view_get``, so YAML cannot
        assert the arch it returns.

        :return: ``None``
        """
        entry = self.env["client_adjustment_entry"]
        for view_type in ("tree", "form"):
            arch = entry.fields_view_get(view_type=view_type)["arch"]
            for attr in ("create", "edit", "delete", "duplicate"):
                self.assertNotIn(
                    '%s="false"' % attr,
                    arch,
                    "Default %s view must not set %s=false" % (view_type, attr),
                )

    def test_readonly_adjustment_entry_views(self):
        """Assert the dedicated AJE views forbid create, edit and delete.

        Pure Python, trigger P1 and limitation L-01: the arch returned by
        ``fields_view_get`` cannot be read from YAML.

        :return: ``None``
        """
        module = "ssi_general_audit_worksheet_uncorrected_aje_analysis"
        entry = self.env["client_adjustment_entry"]
        for view_type in ("tree", "form"):
            view = self.env.ref(
                "%s.client_adjustment_entry_readonly_view_%s" % (module, view_type)
            )
            arch = entry.fields_view_get(view_id=view.id, view_type=view_type)["arch"]
            for attr in ("create", "edit", "delete", "duplicate"):
                self.assertIn(
                    '%s="false"' % attr,
                    arch,
                    "Read-only %s view must set %s=false" % (view_type, attr),
                )
