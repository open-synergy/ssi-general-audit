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

    def test_mus_sampling_walk_matches_spreadsheet_mechanics(self):
        """Pure Python -- HT/26/000687 (2nd revision): faithfully replicate
        ``SD_akun_MUS_terbaru.ods`` sheet ``Data``, columns ``Q18:AA2737``,
        including its reset-on-hit/running-cap state machine -- not a
        textbook cumulative-interval walk.

        With ``multiplier_random`` 0, ``random_start`` (``Data!U2``) is
        pinned to 0.0, making the walk fully deterministic so it can be
        hand-verified against the spreadsheet's own formulas
        (``Data!R18:R2737`` / ``Data!T18:T2737`` / ``Data!AA18:AA2737``):

        - item 0 (900): ``900+0-1=899 < 1000`` -> no hit; position
          continues accumulating to 899.
        - item 1 (800): ``800+899-1=1698 >= 1000`` -> hit; position resets
          to 0 (the random start).
        - item 2 (700): ``700+0-1=699 < 1000`` -> no hit; accumulates to
          699.
        - item 3 (600): ``600+699-1=1298 >= 1000`` -> hit; resets to 0.
        - item 4 (500): ``500-1=499 < 1000`` -> no hit; accumulates to 499.
        - item 5 (400): ``400+499-1=898 < 1000`` -> no hit; accumulates to
          898.
        - item 6 (300): ``300+898-1=1197 >= 1000`` -> hit; resets to 0.
        - items 7-9 (200, 100, 50): none individually nor cumulatively
          reach 1000 again before the list ends.

        So exactly items 1, 3, and 6 are selected -- a plain cumulative
        walk (never resetting) would instead have crossed the 1000
        threshold at cumulative sums 900, 1600 (hit), 700, 1300 (hit),
        800, 1200 (hit), 500, 600, 650: a different set. The running cap
        (``total_planned`` = ``computed_sample_size`` + ``key_count``)
        does not bind here since only 3 hits occur (below the cap), so
        this test does not exercise it -- only the reset-vs-accumulate
        rule.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()
        worksheet.sudo().write({"multiplier_random": 0.0})

        items = [
            {"index": i, "cells": [str(i)], "amount": amount}
            for i, amount in enumerate(
                [900.0, 800.0, 700.0, 600.0, 500.0, 400.0, 300.0, 200.0, 100.0, 50.0]
            )
        ]

        _sorted_items, selected_indices, walk_trace = worksheet._perform_mus_sampling(
            items, key_count=0, sample_interval=1000.0
        )

        self.assertEqual(selected_indices, {1, 3, 6})
        self.assertEqual(worksheet.random_start, 0.0)
        self.assertEqual(worksheet.realized_to_sampling, 3)

        # HT/26/000687 (3rd revision): "From" / "Up To" / "True/False"
        # (``Data!R18:T2737``) are also recorded per item, for display in
        # ``sampling_data``.
        self.assertEqual(walk_trace[0], (0.0, 899.0, False))
        self.assertEqual(walk_trace[1], (899.0, 1698.0, True))
        self.assertEqual(walk_trace[3], (699.0, 1298.0, True))

    def test_mus_sampling_pool_walks_original_order_with_zero_amount_reset(self):
        """Pure Python -- HT/26/000687 (4th revision): two corrections
        verified against ``SD_akun_MUS_terbaru.ods`` sheet ``Data``:

        1. Only the key items (``Data!J18:N2737``'s "Direct Examination"
           rows) are amount-sorted for the walk; the sample pool walks in
           its *original* input order (matching "Sample Examination"),
           not re-sorted by amount -- confirmed by comparing the source
           spreadsheet's population order against its Sample Examination
           row order (only 20 rows differ, exactly the key item count).
        2. A zero-amount item's own From/Up To are blank
           (``Data!R_n = IF(M_n=0,"",...)``), and the *next* item then
           computes ``Up To = IFERROR(amount + blank - 1, 0)`` = 0
           (``Data!S_n``) -- this is what lets "From" resume varying for
           Sample items instead of latching onto ``random_start`` forever
           after the first hit.

        Item 0 (amount 50) comes right after the key item in the walk
        despite items 3/4/5 (300/400/350) being larger -- proving pool
        order is input order, not amount order. Hand-traced with
        ``multiplier_random`` 0 (``random_start`` pinned to 0) so every
        step is deterministic; see the method's docstring for the
        matching Excel cell references.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()
        worksheet.sudo().write({"multiplier_random": 0.0})

        items = [
            {"index": 0, "cells": ["0"], "amount": 50.0},
            {"index": 1, "cells": ["1"], "amount": 1200.0},
            {"index": 2, "cells": ["2"], "amount": 0.0},
            {"index": 3, "cells": ["3"], "amount": 300.0},
            {"index": 4, "cells": ["4"], "amount": 400.0},
            {"index": 5, "cells": ["5"], "amount": 350.0},
        ]

        _sorted_items, selected_indices, walk_trace = worksheet._perform_mus_sampling(
            items, key_count=1, sample_interval=1000.0
        )

        self.assertEqual(selected_indices, set())
        self.assertEqual(walk_trace[1], (0.0, 1199.0, True))  # key item: hit
        self.assertEqual(walk_trace[0], (0.0, 49.0, False))  # pool, original order
        self.assertEqual(walk_trace[2], (None, None, False))  # zero-amount: blank
        self.assertEqual(walk_trace[3], (None, 0.0, False))  # inherits blank -> 0
        self.assertEqual(walk_trace[4], (0.0, 399.0, False))  # accumulation resumes
        self.assertEqual(walk_trace[5], (399.0, 748.0, False))

    def test_mus_sampling_random_start_within_multiplier_random(self):
        """Pure Python -- HT/26/000687 (2nd revision): ``random_start`` is
        drawn from ``[0, Multiplier Random)`` (``Data!U2 = RAND() *
        Multiplier Random``), not clamped to ``sample_interval`` -- run
        many trials since the draw is random.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()
        worksheet.sudo().write({"multiplier_random": 2000000000.0})

        items = [{"index": 0, "cells": ["0"], "amount": 100.0}]

        for _trial in range(50):
            worksheet._perform_mus_sampling(items, key_count=0, sample_interval=1000.0)
            self.assertGreaterEqual(worksheet.random_start, 0.0)
            self.assertLess(worksheet.random_start, 2000000000.0)

    def test_mus_sampling_realized_never_exceeds_total_planned(self):
        """Pure Python -- HT/26/000687 (2nd revision): the running cap
        (``Data!AA18:AA2737`` against ``$U$13+$U$11-1``) must never let
        "Realized to sampling" exceed "Total Plan Examination"
        (``computed_sample_size + key_count``), even when a huge
        ``multiplier_random`` makes almost every item a hit.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()
        worksheet.sudo().write({"multiplier_random": 2000000000.0})

        key_count = 2
        item_count = 10
        item_amount = 100.0
        sample_interval = 300.0
        # 2e9 makes random_start virtually certain to dwarf the 300
        # interval (only a ~1e-7 chance per draw of landing below it),
        # so this deterministically exercises the cap-binding path
        # without flaking across 50 trials.
        worksheet.sudo().write({"multiplier_random": 2000000000.0})
        items = [
            {"index": i, "cells": [str(i)], "amount": item_amount}
            for i in range(item_count)
        ]
        sample_pool_amount = item_amount * (item_count - key_count)
        expected_sample_size = math.floor(sample_pool_amount / sample_interval + 0.5)
        total_planned = expected_sample_size + key_count
        self.assertLess(total_planned, item_count, "test setup must make the cap bind")

        for _trial in range(50):
            (
                _sorted_items,
                selected_indices,
                _walk_trace,
            ) = worksheet._perform_mus_sampling(
                items, key_count=key_count, sample_interval=sample_interval
            )
            self.assertLessEqual(len(selected_indices) + key_count, total_planned)

    def test_cvs_sampling_draws_exactly_the_planned_pool_size(self):
        """Pure Python -- trigger P1 (L-01: ``_perform_simple_random_sample``
        is a private helper with no ``action_*`` wrapper, so its return
        value can't be captured via ``action: call``) and P11 (L-12: no
        loop in YAML for the 50-trial randomness check).

        HT/26/000687 (9th revision, 25 Aug 2026): CVS must draw exactly
        ``total_planned - key_count`` pool rows via ``random.sample``, not
        the earlier per-row independent ``RANDBETWEEN`` acceptance-window
        draw (which could leave "Realized to sampling" short of "Total
        Plan Examination" even with a plentiful pool) -- run many trials
        to check the count is always exact regardless of which rows
        happen to be drawn, and that key item indices never appear in the
        returned (pool-only) selected set.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        key_count = 3
        total_planned = 10
        items = [
            {"index": i, "cells": [str(i)], "amount": float(100 - i)} for i in range(30)
        ]
        key_indices = {
            item["index"]
            for item in sorted(items, key=lambda x: x["amount"], reverse=True)[
                :key_count
            ]
        }

        for _trial in range(50):
            _sorted_items, selected_indices = worksheet._perform_simple_random_sample(
                items, key_count, total_planned
            )
            self.assertEqual(len(selected_indices), total_planned - key_count)
            self.assertTrue(selected_indices.isdisjoint(key_indices))
            self.assertEqual(
                worksheet.realized_to_sampling, key_count + len(selected_indices)
            )

    def test_cvs_sampling_falls_short_only_when_pool_is_too_small(self):
        """Pure Python -- trigger P1 (L-01: ``_perform_simple_random_sample``
        is a private helper with no ``action_*`` wrapper, so its return
        value can't be captured via ``action: call``).

        HT/26/000687 (9th revision, 25 Aug 2026): when the pool has fewer
        rows than the requested sample size, drawing exactly
        ``total_planned - key_count`` rows is impossible, so the draw is
        capped at the pool size and "Realized to sampling" falls short --
        the only case where a CVS variance is expected.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        key_count = 1
        total_planned = 10
        items = [
            {"index": i, "cells": [str(i)], "amount": float(10 - i)} for i in range(4)
        ]

        _sorted_items, selected_indices = worksheet._perform_simple_random_sample(
            items, key_count, total_planned
        )

        self.assertEqual(len(selected_indices), len(items) - key_count)
        self.assertEqual(worksheet.realized_to_sampling, len(items))

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

    def test_apply_where_clause_compares_numeric_columns_by_value(self):
        """HT/26/000687 (7th revision): a column declared ``TEXT`` gets
        TEXT affinity in SQLite, so ``Amount > 10000000`` would compare
        lexicographically -- "4440000" > "10000000" is TRUE as strings
        (leading "4" beats "1"), even though 4,440,000 is not greater
        than 10,000,000. ``_apply_where_clause`` must give an
        all-numeric column NUMERIC affinity instead, so this compares by
        value: only the row above the threshold should survive.
        """
        _admin, worksheet, _gl, _subledger = self._create_worksheet_fixture()

        raw_csv = (
            "Index,Amount,Type\n"
            "0,4440000,Candidate\n"
            "1,10027246,Candidate\n"
            "2,6448273,Candidate\n"
        )

        filtered = worksheet._apply_where_clause(raw_csv, "Amount > 10000000")
        rows = [line for line in filtered.splitlines() if line]

        self.assertEqual(rows, ["Index,Amount,Type", "1,10027246,Candidate"])

    def test_sampling_data_never_lists_nss_candidates(self):
        """HT/26/000687 (6th revision): ``sampling_data`` must only ever
        hold "Key Item" and chosen "Sample" rows -- unchosen "Candidate"
        rows belong in ``nss_candidate_pool`` (used by the "Sampling
        Process" tab), never in the final result.

        Covered here in Python rather than YAML for the same reason as
        ``test_sampling_process_data_excludes_key_items``: no YAML
        substring-absence operator.
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
                "nss_final_sample_size": 1,
            }
        )

        worksheet.action_generate_sampling()

        # Right after generation: nothing chosen yet, so sampling_data has
        # only the key item -- no Candidate rows.
        self.assertIn("Key Item", worksheet.sampling_data)
        self.assertNotIn("Candidate", worksheet.sampling_data)
        self.assertIn("Candidate", worksheet.nss_candidate_pool)

        # After choosing REF002: sampling_data gains it as Sample, but
        # still no Candidate rows (REF002 was the only pool item here).
        worksheet.sudo().write(
            {
                "sampling_process_data": (
                    "Index,ref,amount,note,Type,Chose?\n"
                    "1,REF002,2000,Note 2,Candidate,TRUE\n"
                )
            }
        )

        self.assertIn("REF002", worksheet.sampling_data)
        self.assertNotIn("Candidate", worksheet.sampling_data)
