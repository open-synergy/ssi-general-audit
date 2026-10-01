# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestClientAccountNameSearch(YamlTransactionCase):
    """Name search of ``client_account`` by code and by name."""

    def setUp(self):
        """Create a client, an account group, a type and two accounts."""
        super(TestClientAccountNameSearch, self).setUp()
        env = self.env
        self.client = env["res.partner"].create(
            {"name": "Test Client - Name Search", "is_company": True}
        )
        group = env["client_account_group"].create(
            {
                "name": "Test Group - Name Search",
                "code": "/",
                "sequence": 1,
                "normal_balance": "dr",
            }
        )
        account_type = env["client_account_type"].create(
            {
                "name": "Test Type - Name Search",
                "code": "/",
                "group_id": group.id,
                "sequence": 1,
                "normal_balance": "dr",
                "python_code": "result = 0.0",
            }
        )
        self.account_a = env["client_account"].create(
            {
                "name": "Cash Search",
                "code": " 9.9.1.01 ",
                "partner_id": self.client.id,
                "type_id": account_type.id,
            }
        )
        self.account_b = env["client_account"].create(
            {
                "name": "Bank Search",
                "code": "9.9.1.02",
                "partner_id": self.client.id,
                "type_id": account_type.id,
            }
        )

    def _search(self, text):
        """Return the ids found for ``text`` among the test accounts.

        :param text: text typed in the Many2one autocomplete
        :return: set of ``client_account`` ids
        """
        found = self.env["client_account"].name_search(
            text, args=[("partner_id", "=", self.client.id)]
        )
        return {item[0] for item in found}

    def test_search_by_code(self):
        """Find an account by a part of its code.

        Python only because ``name_search`` returns a value, which
        ``action: call`` drops: ``P1``, ``L-01``.
        """
        self.assertEqual(self._search("9.9.1.01"), {self.account_a.id})
        self.assertEqual(self._search("9.9.1"), {self.account_a.id, self.account_b.id})

    def test_search_by_name(self):
        """Keep finding an account by a part of its name.

        Python only because ``name_search`` returns a value, which
        ``action: call`` drops: ``P1``, ``L-01``.
        """
        self.assertEqual(self._search("Bank"), {self.account_b.id})

    def test_search_without_text(self):
        """Return every account of the client when no text is typed.

        Python only because ``name_search`` returns a value, which
        ``action: call`` drops: ``P1``, ``L-01``.
        """
        self.assertEqual(self._search(""), {self.account_a.id, self.account_b.id})
