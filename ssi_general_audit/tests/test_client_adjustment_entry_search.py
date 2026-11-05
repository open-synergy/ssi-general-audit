# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

SEARCH_FIELDS = (
    "general_audit_id",
    "partner_id",
    "account_type_set_id",
    "currency_id",
    "date_start",
    "date_end",
)
NEW_GROUPS = {
    "grp_general_audit": "general_audit_id",
    "grp_partner": "partner_id",
    "grp_account_type_set": "account_type_set_id",
    "grp_currency": "currency_id",
    "grp_adjustment_type": "adjustment_type",
    "grp_date_start": "date_start",
    "grp_date_end": "date_end",
}
KEPT_GROUPS = ("grp_company", "grp_state", "grp_corrected")


@tagged("post_install", "-at_install")
class TestClientAdjustmentEntrySearch(YamlTransactionCase):
    """Search view of the adjusting journal entry.

    Pure Python test: the check reads the view architecture and runs
    ``read_group``, which the YAML DSL cannot express.
    """

    def _get_arch(self):
        """Get the parsed architecture of the search view.

        :return: the root element of the search view
        """
        model = self.env["client_adjustment_entry"]
        view = model.fields_view_get(
            view_id=self.env.ref(
                "ssi_general_audit.client_adjustment_entry_view_search"
            ).id,
            view_type="search",
        )
        return etree.fromstring(view["arch"])

    def test_search_fields(self):
        """Every Many2one field and the audit dates can be searched.

        Trigger P1, limitation L-01 and L-02 (return value of a method).

        :return: ``None``
        """
        arch = self._get_arch()
        names = arch.xpath("//field/@name")
        for name in SEARCH_FIELDS:
            self.assertIn(name, names)

    def test_group_by_filters(self):
        """New group by filters exist and the existing ones are kept.

        Trigger P1, limitation L-01 and L-02 (return value of a method).

        :return: ``None``
        """
        arch = self._get_arch()
        names = arch.xpath("//filter/@name")
        for name in list(NEW_GROUPS) + list(KEPT_GROUPS):
            self.assertIn(name, names)

    def test_read_group(self):
        """Grouping by every new filter runs without error.

        Trigger P1, limitation L-01 and L-02 (return value of a method).

        :return: ``None``
        """
        model = self.env["client_adjustment_entry"]
        for field_name in NEW_GROUPS.values():
            groups = model.read_group([], ["id"], [field_name])
            self.assertIsInstance(groups, list)
