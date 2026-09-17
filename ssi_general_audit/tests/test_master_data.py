# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestMasterData(YamlTransactionCase):
    def test_master_data(self):
        self.run_yaml_scenario("test_data_master_data.yaml")

    def test_client_financial_ratio_current_ratio_audited(self):
        """Assert Current Ratio's ``python_code`` sets ``result_audited``.

        Pure Python — trigger P1 (L-01: ``call`` discards return values;
        L-03: no YAML action stores an ``EVAL:`` result to the registry).
        ``result_audited`` is a local variable produced by executing the
        ``python_code`` text via ``safe_eval``, exactly as
        ``general_audit_ws_f3a78de.ratio._recompute`` (a model living in a
        different module) does it — it is not a record field, so no YAML
        action can capture or assert it directly on this model.
        Localdict vars available: ``account_group``, ``account_type``.
        Output var read back: ``result_audited``.
        """
        ratio = self.env.ref("ssi_general_audit.client_financial_ratio_1_f0ab3e10")
        localdict = {
            "account_group": {
                "T001": {"audited": 1000.0},
                "T003": {"audited": 500.0},
            },
            "account_type": {},
        }
        safe_eval(ratio.python_code, localdict, mode="exec", nocopy=True)
        self.assertEqual(localdict["result_audited"], 1000.0 / 500.0)

    def test_client_financial_ratio_cash_ratio_audited(self):
        """Assert Cash Ratio's ``python_code`` sets ``result_audited``.

        Pure Python — trigger P1 (L-01, L-03; full rationale under
        ``test_client_financial_ratio_current_ratio_audited``).
        Localdict vars available: ``account_group``, ``account_type``.
        Output var read back: ``result_audited``.
        """
        ratio = self.env.ref("ssi_general_audit.client_financial_ratio_2_30a38c23")
        localdict = {
            "account_group": {"T003": {"audited": 500.0}},
            "account_type": {"S111": {"audited": 300.0}},
        }
        safe_eval(ratio.python_code, localdict, mode="exec", nocopy=True)
        self.assertEqual(localdict["result_audited"], 300.0 / 500.0)

    def test_client_financial_ratio_audited_zero_denominator(self):
        """Assert ``result_audited`` stays 0.0 without an audited T003.

        Negative path for both Current Ratio and Cash Ratio: when
        ``account_group["T003"]["audited"]`` is ``0.0`` or the key is
        absent, the ``audited`` branch must not run and the variable
        keeps its 0.0 initial value. Pure Python — trigger P1 (L-01,
        L-03; full rationale under
        ``test_client_financial_ratio_current_ratio_audited``).
        Localdict vars available: ``account_group``, ``account_type``.
        Output var read back: ``result_audited``.
        """
        current_ratio = self.env.ref(
            "ssi_general_audit.client_financial_ratio_1_f0ab3e10"
        )
        cash_ratio = self.env.ref("ssi_general_audit.client_financial_ratio_2_30a38c23")

        localdict_current = {"account_group": {}, "account_type": {}}
        safe_eval(
            current_ratio.python_code,
            localdict_current,
            mode="exec",
            nocopy=True,
        )
        self.assertEqual(localdict_current["result_audited"], 0.0)

        localdict_cash = {
            "account_group": {"T003": {"audited": 0.0}},
            "account_type": {},
        }
        safe_eval(cash_ratio.python_code, localdict_cash, mode="exec", nocopy=True)
        self.assertEqual(localdict_cash["result_audited"], 0.0)

    def _posture_signed_sum(self, formula, account_group):
        """Sum ``account_group`` amounts per a Posture total formula.

        Reimplements, independently of ``python_code``, the signed-sum
        algorithm ``general_audit_ws_ff42fdc.posture._compute_amounts``
        applies against ``general_audit_ws_ff42fdc.total_formula`` rows
        (module ``ssi_general_audit_worksheet_draft_reporting``, not a
        dependency of this module, so the model itself cannot be
        instantiated here). ``formula`` mirrors the ``group_id``/``sign``
        pairs recorded for ``profit_after_tax``/``comprehensive_profit``
        in ``data/master/general_audit_ws_ff42fdc_total_formula.xml``.

        :param formula: list of ``(client_account_group.code, sign)``
            pairs, ``sign`` being ``1`` for "add" or ``-1`` for
            "subtract".
        :param account_group: mapping of group code to amount.
        :return: signed sum as a float.
        """
        return sum(sign * account_group.get(code, 0.0) for code, sign in formula)

    def test_trial_balance_computation_item_tax_expense(self):
        """Assert Tax Expense's ``python_code`` reads group T014 as-is.

        Pure Python — trigger P1 (L-01: ``call`` discards return values;
        L-03: no YAML action stores an ``EVAL:`` result to the
        registry), same rationale as
        ``test_client_financial_ratio_current_ratio_audited``.
        Localdict var available: ``account_group``.
        Output var read back: ``result``.
        """
        item = self.env.ref(
            "ssi_general_audit.trial_balance_computation_item_30_b40ad860"
        )
        localdict = {
            "account_group": {
                "T009": 100.0,
                "T010": 10.0,
                "T011": 30.0,
                "T012": 20.0,
                "T013": 5.0,
                "T014": 11.0,
                "T015": 4.0,
            },
        }
        safe_eval(item.python_code, localdict, mode="exec", nocopy=True)
        self.assertEqual(localdict["result"], 11.0)

    def test_trial_balance_computation_item_total_net_profit(self):
        """Assert Total Net Profit matches Posture's Profit After Tax.

        Pure Python — trigger P1 (L-01, L-03; full rationale under
        ``test_client_financial_ratio_current_ratio_audited``). The
        expected value is not a bare literal: it is cross-checked
        against ``_posture_signed_sum`` applying the same
        ``group_id``/``sign`` pairs configured for ``total_type =
        "profit_after_tax"`` in
        ``general_audit_ws_ff42fdc_total_formula.xml`` (T009/T010 add,
        T011/T012/T013/T014 subtract), so a drift between this item's
        ``python_code`` and Posture's formula fails here even if both
        happen to evaluate to the same literal number.
        Localdict var available: ``account_group``.
        Output var read back: ``result``.
        """
        item = self.env.ref(
            "ssi_general_audit.trial_balance_computation_item_31_ec987fd9"
        )
        account_group = {
            "T009": 100.0,
            "T010": 10.0,
            "T011": 30.0,
            "T012": 20.0,
            "T013": 5.0,
            "T014": 11.0,
            "T015": 4.0,
        }
        localdict = {"account_group": account_group}
        safe_eval(item.python_code, localdict, mode="exec", nocopy=True)
        profit_after_tax = self._posture_signed_sum(
            [
                ("T009", 1),
                ("T010", 1),
                ("T011", -1),
                ("T012", -1),
                ("T013", -1),
                ("T014", -1),
            ],
            account_group,
        )
        self.assertEqual(localdict["result"], 44.0)
        self.assertEqual(localdict["result"], profit_after_tax)

    def test_trial_balance_computation_item_total_net_profit_and_oci(self):
        """Assert Total Net Profit & OCI matches Comprehensive Profit.

        Pure Python — trigger P1 (L-01, L-03; full rationale under
        ``test_client_financial_ratio_current_ratio_audited``). The
        expected value is cross-checked against ``_posture_signed_sum``
        applying the ``group_id``/``sign`` pairs configured for
        ``total_type = "comprehensive_profit"`` in
        ``general_audit_ws_ff42fdc_total_formula.xml`` (same as Profit
        After Tax, plus T015 add), mirroring
        ``test_trial_balance_computation_item_total_net_profit``.
        Localdict var available: ``account_group``.
        Output var read back: ``result``.
        """
        item = self.env.ref(
            "ssi_general_audit.trial_balance_computation_item_32_c046e7f5"
        )
        account_group = {
            "T009": 100.0,
            "T010": 10.0,
            "T011": 30.0,
            "T012": 20.0,
            "T013": 5.0,
            "T014": 11.0,
            "T015": 4.0,
        }
        localdict = {"account_group": account_group}
        safe_eval(item.python_code, localdict, mode="exec", nocopy=True)
        comprehensive_profit = self._posture_signed_sum(
            [
                ("T009", 1),
                ("T010", 1),
                ("T011", -1),
                ("T012", -1),
                ("T013", -1),
                ("T014", -1),
                ("T015", 1),
            ],
            account_group,
        )
        self.assertEqual(localdict["result"], 48.0)
        self.assertEqual(localdict["result"], comprehensive_profit)
