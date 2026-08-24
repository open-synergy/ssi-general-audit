# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import math

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSa916660(YamlTransactionCase):
    """Cover CRUD, compute, and onchange for ``general_audit_ws_a916660``."""

    def test_general_audit_ws_a916660(self):
        """Run the YAML scenario covering this worksheet."""
        self.run_yaml_scenario("test_data_general_audit_ws_a916660.yaml")

    def _create_worksheet_fixture(self):
        """Build the minimal general_audit + GL + Subledger + worksheet
        fixture needed by the Python-only onchange tests below, entirely
        through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - A916660 Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - A916660 Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-A916660-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - A916660 Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - A916660 Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - A916660 Python",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": account_type_set.id,
                    "financial_accounting_standard_id": standard.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        audit.with_user(admin).action_open()

        ws_type = env.ref(
            "ssi_general_audit_worksheet_sample_determination.worksheet_type_a916660"
        )
        ws_type_d209914 = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        ws_type_b5e3d9f = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_b5e3d9f"
        )
        gl = (
            env["general_audit_ws_d209914"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_d209914.id})
        )
        subledger = (
            env["general_audit_ws_b5e3d9f"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type_b5e3d9f.id})
        )
        worksheet = (
            env["general_audit_ws_a916660"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )
        return admin, worksheet, gl, subledger

    def test_onchange_data_mode_clears_general_ledger_id(self):
        """Pure Python -- trigger P12 (L-20: ``Form`` only via
        ``action: form``, no ``view`` key -- view-specific onchange
        behaviour is unreachable from YAML).

        ``onchange_general_ledger_id`` is declared
        ``@api.onchange("data_mode")``. Unlike the sibling
        ``general_audit_ws_c6c86fd`` / ``general_audit_ws_b4f7d9c`` cases,
        ``data_mode`` and ``general_ledger_id`` are *not* mutually exclusive
        by state here -- both share the exact same
        ``states={"open": [("readonly", False)]}`` definition. Driving this
        through ``action: form`` in YAML was tried first, but CI proved it
        fails unconditionally on this model's form view with
        ``AssertionError: __len__ was not found in the view`` regardless of
        which field is touched -- caused by the mixin-level
        ``allowed_general_ledger_ids`` / ``allowed_subledger_ids`` Many2many
        fields being declared ``invisible="1"`` with no sub-view/tree arch,
        which the ``Form`` test helper cannot build editable metadata for.
        That is a pre-existing limitation of the shared worksheet mixin's
        view, not something this test suite is allowed to fix (production
        code is out of scope). The onchange method is called directly here
        instead, to verify its own body does what it claims.
        """
        _admin, worksheet, gl, _subledger = self._create_worksheet_fixture()

        worksheet.sudo().write({"data_mode": "gl", "general_ledger_id": gl.id})
        self.assertTrue(worksheet.general_ledger_id)

        worksheet.onchange_general_ledger_id()

        self.assertFalse(worksheet.general_ledger_id)

    def test_onchange_data_mode_clears_subledger_id(self):
        """Pure Python -- trigger P12 (L-20), see
        ``test_onchange_data_mode_clears_general_ledger_id`` for why this
        onchange is verified by calling the method directly instead of
        through ``Form``.
        """
        _admin, worksheet, _gl, subledger = self._create_worksheet_fixture()

        worksheet.sudo().write({"data_mode": "subledger", "subledger_id": subledger.id})
        self.assertTrue(worksheet.subledger_id)

        worksheet.onchange_subledger_id()

        self.assertFalse(worksheet.subledger_id)

    def test_onchange_tolerable_misstatement_cvs(self):
        """Pure Python -- trigger P12 (L-20), see
        ``test_onchange_data_mode_clears_general_ledger_id`` for why this
        onchange is verified by calling the method directly instead of
        through ``Form``.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        worksheet.sudo().write(
            {
                "method_type": "cvs",
                "performance_materiality": 10000.0,
                "risk_factor": 0.9,
            }
        )
        self.assertEqual(worksheet.tolerable_misstatement, 0.0)

        worksheet.onchange_tolerable_misstatement()

        self.assertEqual(worksheet.tolerable_misstatement, 9000.0)

    def test_onchange_tolerable_misstatement_mus(self):
        """Pure Python -- trigger P12 (L-20), see
        ``test_onchange_data_mode_clears_general_ledger_id`` for why this
        onchange is verified by calling the method directly instead of
        through ``Form``.

        HT/26/000687: MUS now follows the same "Input Variabel" pattern as
        CVS/NSS (Performance Materiality x Risk Factor -> Tolerable
        Misstatement) instead of being left untouched.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        worksheet.sudo().write(
            {
                "method_type": "mus",
                "performance_materiality": 10000.0,
                "risk_factor": 0.9,
                "tolerable_misstatement": 500.0,
            }
        )

        worksheet.onchange_tolerable_misstatement()

        self.assertEqual(worksheet.tolerable_misstatement, 9000.0)

    def test_onchange_reliability_factor(self):
        """Pure Python -- trigger P12 (L-20), see
        ``test_onchange_data_mode_clears_general_ledger_id`` for why this
        onchange is verified by calling the method directly instead of
        through ``Form``.

        HT/26/000687: ``reliability_factor`` is now a plain editable field
        (no longer a ``compute``); the ``RELIABILITY_FACTOR_TABLE`` lookup
        only runs as a UI default suggestion via this onchange.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        worksheet.sudo().write({"confidence_level": "90"})
        self.assertEqual(worksheet.reliability_factor, 0.0)

        worksheet.onchange_reliability_factor()

        self.assertEqual(worksheet.reliability_factor, 2.31)

    def test_mus_sampling_realized_matches_planned(self):
        """Pure Python -- HT/26/000687: "Realized to sampling" must always
        match "Total Plan Examination".

        Before the fix, the random start was drawn from the full
        ``[0, sample_interval)`` range: a start landing close to the
        interval could walk past the last item's cumulative amount before
        reaching the final threshold, silently realizing one fewer hit
        than ``math.ceil(total / sample_interval)`` planned. Run many
        trials since the random start is what triggers the bug.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        items = [
            {"index": i, "cells": [str(i)], "amount": amount}
            for i, amount in enumerate(
                [
                    237000.0,
                    154000.0,
                    98000.0,
                    61000.0,
                    45000.0,
                    33000.0,
                    21000.0,
                    15000.0,
                ]
            )
        ]
        sample_interval = 50000.0
        total_amount = sum(item["amount"] for item in items)
        expected_size = math.ceil(total_amount / sample_interval)

        for _trial in range(50):
            _sorted_items, selected_indices = worksheet._perform_mus_sampling(
                items, key_count=0, sample_interval=sample_interval
            )
            self.assertEqual(len(selected_indices), expected_size)

    def test_sampling_process_data_excludes_key_items(self):
        """HT/26/000687: the "Sampling Process" tab (NSS) must only show
        "Candidate" rows -- "Key Item" rows are chosen automatically and
        are not part of the manual selection process.

        Covered here in Python rather than YAML because the assertion
        needs a substring *absence* check, which the YAML scenario
        runner's ``_VALID_OPERATORS`` does not offer (only ``contains``,
        no ``not_contains``).
        """
        _admin, worksheet, gl, _subledger = self._create_worksheet_fixture()
        gl.sudo().write(
            {
                "raw_data": (
                    "ref,amount,note\n" "REF001,1000,Note 1\n" "REF002,2000,Note 2\n"
                )
            }
        )
        worksheet.sudo().write(
            {
                "data_mode": "gl",
                "general_ledger_id": gl.id,
                "identifier_col_number": 1,
                "monetary_col_number": 2,
                "additional_info_col_number": 3,
                "key_item_count": 1,
                "method_type": "nss",
            }
        )

        worksheet.action_generate_sampling()

        self.assertIn("REF001", worksheet.sampling_process_data)
        self.assertNotIn("REF002", worksheet.sampling_process_data)
        self.assertNotIn("Key Item", worksheet.sampling_process_data)
