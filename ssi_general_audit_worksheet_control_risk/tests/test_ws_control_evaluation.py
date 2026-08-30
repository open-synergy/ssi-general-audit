# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


def _load_migration_module():
    """Import ``post-migrate.py`` (issue #299) as a plain module.

    The migrations directory name (``14.0.2.8.0``) is not a valid
    Python package/module identifier (leading digits, dots), so it
    cannot be reached with a normal ``import`` statement -- it has to
    be loaded from its file path via :mod:`importlib.util`.

    :return: the loaded module object exposing ``migrate(env, version)``
    """
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, "migrations", "14.0.2.8.0", "post-migrate.py")
    spec = importlib.util.spec_from_file_location(
        "test_ws_f63f569_post_migrate_14_0_2_8_0", path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@tagged("post_install", "-at_install")
class TestWSControlEvaluation(YamlTransactionCase):
    """Scenario tests for the IT Control Evaluation worksheet (f63f569)."""

    def test_ws_control_evaluation(self):
        """Run the workflow/master-data scenarios for f63f569."""
        self.run_yaml_scenario("test_data_ws_control_evaluation.yaml")

    def test_migration_14_0_2_8_0_restructures_existing_worksheet(self):
        """Restructure an old-shape f63f569 worksheet, twice, safely.

        Pure Python -- trigger P10 (L-09, L-11: exercising the actual
        migration logic requires importing
        ``migrations/14.0.2.8.0/post-migrate.py`` via
        :mod:`importlib`, which the YAML DSL's ``EVAL:`` sandbox
        forbids outright -- there is no ``import`` in its whitelist,
        and no YAML action can invoke an arbitrary non-model function
        in the first place).

        Builds a worksheet whose ``.detail``/``.indicator`` lines
        mirror the pre-fix bug: every indicator of category 5 (Input
        Controls) hangs off a single placeholder detail row on
        control A, with ``result`` already answered on some lines.
        After running ``migrate()``, the indicators must be spread
        across the 4 real controls of that category while keeping
        their ``result``, and a second run must not create duplicate
        detail rows (idempotency).
        """
        migration = _load_migration_module()

        ws_type_f63f569 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk." "worksheet_type_f63f569",
            raise_if_not_found=False,
        )
        self.assertTrue(ws_type_f63f569, "worksheet type f63f569 must exist")

        control_a = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_159_d1cc860b"
        )
        control_b = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_312_d04705fa"
        )
        control_c = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_313_28261117"
        )
        control_d = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_314_e52ce723"
        )
        indicator_249 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_249_c658faa5"
        )
        indicator_250 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_250_4255f814"
        )
        indicator_251 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_251_4976bbd2"
        )
        indicator_252 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_252_a8154cd6"
        )
        indicator_253 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_253_6abec5a9"
        )
        indicator_254 = self.env.ref(
            "ssi_general_audit_worksheet_control_risk."
            "general_audit_it_control_indicator_254_0d5747d0"
        )
        yes_option = indicator_249.option_set_id.option_ids[:1]
        self.assertTrue(yes_option, "the indicator option set must offer a choice")

        # Shared fixture recipe for `general_audit` in state "open" --
        # see ssi_general_audit/tests/README_FIXTURE.md. Everything runs
        # as `base.user_admin` (not the default SUPERUSER_ID env): the
        # policy check behind `action_open` allows the record's own
        # creator or a validator-group member, and OdooBot (uid=1,
        # SUPERUSER_ID) is a member of no group at all.
        admin_user = self.env.ref("base.user_admin")
        env = self.env(user=admin_user)
        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = env["res.partner"].create(
            {"name": "Test Migration 299 Client", "is_company": True}
        )
        accountant = env["res.partner"].create(
            {"name": "Test Migration 299 Accountant"}
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-MIG299-0001",
            }
        )
        account_type_set = env["client_account_type_set"].create(
            {"name": "Test Migration 299 Account Type Set", "code": "/"}
        )
        standard = env["accountant.financial_accounting_standard"].create(
            {"name": "Test Migration 299 Standard", "code": "/"}
        )
        audit = env["general_audit"].create(
            {
                "title": "Test Migration 299 - IT Control",
                "partner_id": client.id,
                "accountant_id": accountant.id,
                "account_type_set_id": account_type_set.id,
                "financial_accounting_standard_id": standard.id,
                "date_start": "2024-01-01",
                "date_end": "2024-12-31",
                "need_interim": False,
                "need_previous": False,
                "num_of_consecutive_audit_firm": 1,
                "num_of_consecutive_audit_accountant": 1,
            }
        )
        audit.action_open()
        audit.invalidate_cache()
        worksheet = env["general_audit_ws_f63f569"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type_f63f569.id,
            }
        )
        old_detail = env["general_audit_ws_f63f569.detail"].create(
            {
                "worksheet_id": worksheet.id,
                "control_id": control_a.id,
            }
        )
        line_249 = env["general_audit_ws_f63f569.indicator"].create(
            {
                "detail_id": old_detail.id,
                "indicator_id": indicator_249.id,
                "result": yes_option.id,
            }
        )
        line_250 = env["general_audit_ws_f63f569.indicator"].create(
            {
                "detail_id": old_detail.id,
                "indicator_id": indicator_250.id,
                "result": yes_option.id,
            }
        )
        line_251 = env["general_audit_ws_f63f569.indicator"].create(
            {"detail_id": old_detail.id, "indicator_id": indicator_251.id}
        )
        line_252 = env["general_audit_ws_f63f569.indicator"].create(
            {"detail_id": old_detail.id, "indicator_id": indicator_252.id}
        )
        line_253 = env["general_audit_ws_f63f569.indicator"].create(
            {
                "detail_id": old_detail.id,
                "indicator_id": indicator_253.id,
                "result": yes_option.id,
            }
        )
        line_254 = env["general_audit_ws_f63f569.indicator"].create(
            {"detail_id": old_detail.id, "indicator_id": indicator_254.id}
        )

        migration.migrate(self.env.cr, "14.0.2.8.0")

        details = self.env["general_audit_ws_f63f569.detail"].search(
            [("worksheet_id", "=", worksheet.id)]
        )
        self.assertEqual(
            len(details),
            4,
            "category 5 has 4 real controls, so restructuring must "
            "split the single placeholder detail into 4 detail lines",
        )

        self.assertEqual(line_249.detail_id.control_id, control_a)
        self.assertEqual(line_249.result, yes_option)

        self.assertEqual(line_250.detail_id.control_id, control_b)
        self.assertEqual(line_251.detail_id.control_id, control_b)
        self.assertEqual(line_252.detail_id.control_id, control_b)
        self.assertEqual(line_250.detail_id, line_251.detail_id)
        self.assertEqual(line_251.detail_id, line_252.detail_id)

        self.assertEqual(line_253.detail_id.control_id, control_c)
        self.assertEqual(line_253.result, yes_option)

        self.assertEqual(line_254.detail_id.control_id, control_d)

        migration.migrate(self.env.cr, "14.0.2.8.0")

        details_after_rerun = self.env["general_audit_ws_f63f569.detail"].search(
            [("worksheet_id", "=", worksheet.id)]
        )
        self.assertEqual(
            len(details_after_rerun),
            4,
            "re-running the migration must not create duplicate detail " "lines",
        )
