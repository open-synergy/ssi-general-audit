# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

from .ui_fixture import create_populate_worksheet


@tagged("post_install", "-at_install")
class TestGeneralAuditWSf5a3cee(YamlTransactionCase):
    """Tests of the Data Collection worksheet (f5a3cee)."""

    def test_general_audit_ws_f5a3cee(self):
        """Run the Data Collection worksheet scenarios."""
        self.run_yaml_scenario("test_data_ws_f5a3cee.yaml")

    def test_populate_splits_permanent_and_current(self):
        """Fill each file list only with the items of its own type.

        Python-only test, trigger P10 (limitation L-11): the types of all
        lines of a one2many cannot be asserted in a YAML scenario.
        """
        worksheet = create_populate_worksheet(self.env, "F5A3CEE-ORDER")
        self.env["general_audit_data_collection"].create(
            {
                "name": "Order current item",
                "code": "0-TOUR-CF",
                "type": "current_file",
                "category_id": self.env.ref(
                    "ssi_general_audit_worksheet_client_package"
                    ".general_audit_data_collection_category_1_ffbc1f1d"
                ).id,
            }
        )
        worksheet.action_populate_details()
        worksheet.invalidate_cache()
        self.assertEqual(
            set(worksheet.permanent_ids.mapped("data_collection_type")),
            {"permanent_file"},
        )
        self.assertEqual(
            set(worksheet.current_ids.mapped("data_collection_type")),
            {"current_file"},
        )
        self.assertFalse(worksheet.reporting_timetable_ids)
