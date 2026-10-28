# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from types import SimpleNamespace

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


class _FakeDetails(list):
    """List of fake account details that supports ``filtered``."""

    def filtered(self, func):
        """Filter the fake details like a recordset does.

        :param func: predicate called with each fake detail
        :return: a new fake list with the matching details
        """
        return _FakeDetails(d for d in self if func(d))


@tagged("post_install", "-at_install")
class TestGeneralAuditClosingAmount(YamlTransactionCase):
    """Test the sign logic of the closing mapping amount."""

    def _make_type(self, name, group, normal_balance):
        """Create an account type.

        :param name: type name
        :param group: ``client_account_group`` record of the type
        :param normal_balance: ``dr`` or ``cr``
        :return: the new ``client_account_type`` record
        """
        return self.env["client_account_type"].create(
            {
                "name": name,
                "code": "/",
                "group_id": group.id,
                "normal_balance": normal_balance,
            }
        )

    def _compute(self, mapping, details):
        """Compute the mapping amount for fake account details.

        :param mapping: closing mapping record
        :param details: list of ``(type, normal_balance, audited_balance)``
            tuples, one per account
        :return: the closing amount as a float
        """
        audit = SimpleNamespace(
            detail_ids=_FakeDetails(
                SimpleNamespace(
                    type_id=t,
                    account_id=SimpleNamespace(normal_balance=nb),
                    audited_balance=b,
                )
                for t, nb, b in details
            )
        )
        return mapping._compute_closing_amount(audit)

    def test_closing_amount_sign(self):
        """Credit accounts add, debit accounts subtract, others are ignored.

        Pure Python test: the audited balance of an account line is a
        stored related field of the trial balance, so the scenario is
        built with fake lines. Trigger P6, limitation L-15 (no mock or
        stub in the YAML DSL).

        :return: ``None``
        """
        group = self.env["client_account_group"].create(
            {"name": "Test Type Group", "code": "/", "normal_balance": "cr"}
        )
        revenue = self._make_type("Test Revenue", group, "cr")
        expense = self._make_type("Test Expense", group, "dr")
        other = self._make_type("Test Other", group, "cr")
        closing_type = self.env["general_audit_closing_type"].create(
            {"name": "Test Closing Type", "code": "/"}
        )
        mapping = self.env["general_audit_closing_type.mapping"].create(
            {
                "closing_type_id": closing_type.id,
                "name": "Close profit and loss",
                "source_type_ids": [(6, 0, [revenue.id, expense.id])],
                "account_type_id": other.id,
            }
        )
        details = [
            (revenue, "cr", 70.0),
            (revenue, "cr", 30.0),
            (expense, "dr", 40.0),
            (other, "cr", 999.0),
        ]
        self.assertEqual(self._compute(mapping, details), 60.0)
        details = [(revenue, "cr", 10.0), (expense, "dr", 40.0)]
        self.assertEqual(self._compute(mapping, details), -30.0)
        self.assertEqual(self._compute(mapping, []), 0.0)
