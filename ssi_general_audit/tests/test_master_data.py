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
