# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSLeadSchedule(YamlTransactionCase):
    def test_ws_lead_schedule(self):
        self.run_yaml_scenario("test_data_ws_lead_schedule.yaml")

    def test_detail_lines_are_ordered_by_account_code(self):
        """Detail lines are sorted by account code, then by id.

        Pure Python -- trigger P3 (L-06: the row order of an o2m cannot
        be asserted from YAML). The sort key is the stored copy of the
        account code, as ``client_account`` is not ordered by code alone.

        :return: nothing; asserts the sort key and the stored field
        """
        detail = self.env["general_audit_ws_b26d482.detail"]
        self.assertEqual(detail._order, "account_code, id")
        field = detail._fields["account_code"]
        self.assertTrue(field.store)
        self.assertEqual(field.related, ("account_id", "code"))
