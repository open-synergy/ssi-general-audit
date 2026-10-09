# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSDraftReporting(YamlTransactionCase):
    """Scenario tests for the ``ssi_general_audit_worksheet_draft_reporting``
    worksheets."""

    # Every ``client_account_group`` code listed by the seeded
    # ``general_audit_ws_ff42fdc.layout_line`` records as a "group" line,
    # mapped to its data XML ID in ``ssi_general_audit``. T008 is not in the
    # seeded layout, so it is left out here too.
    _GROUP_XML_IDS = {
        "T001": "ssi_general_audit.client_account_group_1_885ef902",
        "T002": "ssi_general_audit.client_account_group_2_becd85c2",
        "T003": "ssi_general_audit.client_account_group_3_8f77474a",
        "T004": "ssi_general_audit.client_account_group_4_8512d9b0",
        "T005": "ssi_general_audit.client_account_group_5_7f3c394c",
        "T006": "ssi_general_audit.client_account_group_6_76ade538",
        "T007": "ssi_general_audit.client_account_group_7_fd2a0509",
        "T009": "ssi_general_audit.client_account_group_9_7849ad25",
        "T010": "ssi_general_audit.client_account_group_10_04a8da99",
        "T011": "ssi_general_audit.client_account_group_11_44410d3c",
        "T012": "ssi_general_audit.client_account_group_12_ae0c12b7",
        "T013": "ssi_general_audit.client_account_group_13_1da08e35",
        "T014": "ssi_general_audit.client_account_group_14_aad3d348",
        "T015": "ssi_general_audit.client_account_group_15_315c4d27",
    }

    def test_ws_draft_reporting(self):
        """Run the CRUD/workflow/posture-aggregation YAML scenarios."""
        self.run_yaml_scenario("test_data_ws_draft_reporting.yaml")

    def _create_general_audit_for_posture(self, name_suffix):
        """Create and open a minimal ``general_audit`` for posture tests.

        Fixture built in Python (P10: this is shared setup for several
        Python-only test methods below, and the YAML scenario registry
        used by ``run_yaml_scenario`` does not survive into a plain
        ``TransactionCase`` method -- aturan penulisan #6 in
        ``python-escape-hatch.md``).

        :param str name_suffix: text appended to record names so
            fixtures from different test methods stay distinguishable
        :return: the ``general_audit`` record, already opened
        :rtype: recordset
        """
        config_parameter = self.env["ir.config_parameter"].sudo()
        config_parameter.set_param("ssi_general_audit.max_number_of_cpa_license", "100")

        client = self.env["res.partner"].create(
            {
                "name": "Test Audit Client - %s" % name_suffix,
                "is_company": True,
            }
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Audit Accountant - %s" % name_suffix}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-%s-0001" % name_suffix,
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test Account Type Set - %s" % name_suffix, "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {
                "name": "Test Financial Accounting Standard - %s" % name_suffix,
                "code": "/",
            }
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Test General Audit - %s" % name_suffix,
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
        audit.action_open()
        return audit

    def _create_ff42fdc_worksheet(self, audit):
        """Create and open a ``general_audit_ws_ff42fdc`` for ``audit``.

        :param recordset audit: the parent ``general_audit`` record
        :return: the worksheet record, already opened
        :rtype: recordset
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_ff42fdc"
        )
        worksheet = self.env["general_audit_ws_ff42fdc"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type.id,
            }
        )
        worksheet.action_open()
        return worksheet

    def _create_ff42fdc_worksheet_with_all_groups(self):
        """Build a ff42fdc worksheet whose audit covers every layout group.

        Maps one ``client_account`` per code in ``_GROUP_XML_IDS`` onto
        the General Audit (via ``client_account_mapping`` +
        ``action_reload_account``), so ``detail_ids.account_id.group_id``
        covers every "group" entry of the seeded layout. No trial
        balance/adjustment data is created: this fixture is only used to
        assert the count/sequence/order of ``posture_ids``, never the
        Unaudited/Audited amounts, so the amounts are left at zero.

        :return: the opened worksheet, with its audit's account mapping
            reloaded
        :rtype: recordset
        """
        audit = self._create_general_audit_for_posture("Posture Resequence All Groups")
        client = audit.partner_id

        mapping = self.env["client_account_mapping"].create(
            {"general_audit_id": audit.id}
        )
        for code, xml_id in self._GROUP_XML_IDS.items():
            group = self.env.ref(xml_id)
            account_type = self.env["client_account_type"].create(
                {
                    "name": "Test Account Type %s - Posture Resequence" % code,
                    "code": "/",
                    "group_id": group.id,
                    "normal_balance": "dr",
                    # DILARANG membiarkan python_code pada default
                    # "result = document.balance": lihat catatan yang
                    # sama di test_data_ws_draft_reporting.yaml.
                    "python_code": "result = 0.0",
                }
            )
            account = self.env["client_account"].create(
                {
                    "name": "Test Client Account %s - Posture Resequence" % code,
                    "code": "ACC-%s-POSTURE-RESEQ" % code,
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
            self.env["client_account_mapping.detail"].create(
                {"mapping_id": mapping.id, "account_id": account.id}
            )

        audit.action_reload_account()
        return self._create_ff42fdc_worksheet(audit)

    def test_action_load_posture_first_reload_sequence_and_order(self):
        """A single ``action_load_posture`` call already sorts ``posture_ids``.

        Pure Python -- trigger P3 (L-06: ``odoo-yaml-test`` compares
        o2m/m2m fields as unordered sets, so the row order of
        ``posture_ids`` can never be asserted from YAML). Reproduces the
        "Posture Report berantakan pada Reload pertama" bug: before the
        fix, reading ``worksheet.posture_ids`` right after a single
        ``action_load_posture()`` call returned the lines in creation
        order (every newly created Account Group line, then every newly
        created Total line) instead of layout order,
        because ``Many2one._update_inverses`` (``odoo/fields.py``)
        appends newly created records to the worksheet's already-cached
        ``posture_ids`` tuple instead of re-querying with
        ``_order = "sequence, id"``.

        :return: nothing; asserts count, per-line ``sequence``, and
            that ``posture_ids`` reads back already sorted
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()

        worksheet.action_load_posture()

        layout = self.env["general_audit_ws_ff42fdc.layout_line"].search([])
        order_index = {
            line._layout_key(): position for position, line in enumerate(layout)
        }
        expected_count = len(self._GROUP_XML_IDS) + 9
        self.assertEqual(len(worksheet.posture_ids), expected_count)

        for posture in worksheet.posture_ids:
            key = posture._posture_line_order_key()
            self.assertIn(key, order_index)
            self.assertEqual(posture.sequence, order_index[key] * 10)

        sequences = worksheet.posture_ids.mapped("sequence")
        self.assertEqual(
            sequences,
            sorted(sequences),
            "posture_ids must already read back sorted by sequence "
            "right after a single action_load_posture() call, with no "
            "second Reload and no manual invalidate_cache()",
        )

    def test_action_load_posture_reread_after_cache_invalidation(self):
        """A fresh, cache-invalidated read is sorted after one Reload too.

        Pure Python -- trigger P3 (L-06: order can never be asserted
        from YAML). Complements
        ``test_action_load_posture_first_reload_sequence_and_order`` by
        covering the other reads the Kriteria Penerimaan calls out:
        ``invalidate_cache()`` followed by ``posture_ids``, and a brand
        new ``search()`` on the comodel.

        :return: nothing; asserts both re-read paths come back sorted
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()

        worksheet.action_load_posture()

        worksheet.invalidate_cache(fnames=["posture_ids"], ids=worksheet.ids)
        reread_sequences = worksheet.posture_ids.mapped("sequence")
        self.assertEqual(reread_sequences, sorted(reread_sequences))

        searched = self.env["general_audit_ws_ff42fdc.posture"].search(
            [("worksheet_id", "=", worksheet.id)]
        )
        searched_sequences = searched.mapped("sequence")
        self.assertEqual(searched_sequences, sorted(searched_sequences))

    def test_action_load_posture_without_detail_still_orders_totals(self):
        """Reload with no audit detail still yields 9 ordered Total lines.

        Pure Python -- trigger P3 (L-06: order assertion). Negative
        path from the issue's Skenario Uji: a General Audit with no
        ``detail_ids`` at all must still produce the nine fixed Total
        lines (all zero), without error, and already correctly ordered
        after one ``action_load_posture()`` call.

        :return: nothing; asserts count, zero amounts, and order
        """
        audit = self._create_general_audit_for_posture("Posture Resequence No Detail")
        worksheet = self._create_ff42fdc_worksheet(audit)

        worksheet.action_load_posture()

        self.assertEqual(len(worksheet.posture_ids), 9)
        self.assertTrue(
            all(posture.line_type == "total" for posture in worksheet.posture_ids)
        )
        self.assertTrue(
            all(posture.unaudited == 0.0 for posture in worksheet.posture_ids)
        )

        sequences = worksheet.posture_ids.mapped("sequence")
        self.assertEqual(sequences, sorted(sequences))

    def _posture_sequence_by_code(self, worksheet):
        """Map each posture line code to its ``sequence``.

        :param recordset worksheet: the ff42fdc worksheet
        :return: ``{code: sequence}``, where ``code`` is the group code
            for Account Group lines and the total type for Total lines
        :rtype: dict
        """
        return {
            posture._posture_line_order_key()[1]: posture.sequence
            for posture in worksheet.posture_ids
        }

    def test_layout_places_other_equity_between_capital_and_retained(self):
        """The seeded layout puts T006 between T005 and T007.

        Pure Python -- trigger P3 (L-06: order assertion).

        :return: nothing; asserts the relative order of three groups
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()

        worksheet.action_load_posture()

        sequence = self._posture_sequence_by_code(worksheet)
        self.assertLess(sequence["T005"], sequence["T006"])
        self.assertLess(sequence["T006"], sequence["T007"])

    def test_layout_change_reorders_posture_on_reload(self):
        """Editing a layout line changes the order after the next Reload.

        Pure Python -- trigger P3 (L-06: order assertion). Moves T006
        to the top of the layout and reloads a worksheet that was
        already loaded.

        :return: nothing; asserts T006 becomes the first posture line
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()
        worksheet.action_load_posture()
        layout_t006 = self.env["general_audit_ws_ff42fdc.layout_line"].search(
            [("line_type", "=", "group"), ("group_id.code", "=", "T006")]
        )
        layout_t006.sequence = -10

        worksheet.action_load_posture()

        sequence = self._posture_sequence_by_code(worksheet)
        self.assertEqual(sequence["T006"], min(sequence.values()))
        self.assertEqual(worksheet.posture_ids[0].group_id.code, "T006")

    def test_group_missing_from_layout_is_shown_last(self):
        """A group without a layout line is still shown, after all others.

        Pure Python -- trigger P3 (L-06: order assertion). Deletes the
        T006 layout line, which stands for a group added later.

        :return: nothing; asserts T006 is the last posture line
        """
        self.env["general_audit_ws_ff42fdc.layout_line"].search(
            [("line_type", "=", "group"), ("group_id.code", "=", "T006")]
        ).unlink()
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()

        worksheet.action_load_posture()

        sequence = self._posture_sequence_by_code(worksheet)
        self.assertEqual(sequence["T006"], max(sequence.values()))

    def _create_b555edd_worksheet(self, suffix, need_previous=False):
        """Create a ``general_audit_ws_b555edd`` on a fresh General Audit.

        :param str suffix: text that keeps the fixtures distinguishable
        :param bool need_previous: whether the audit keeps a previous period
        :return: the worksheet record
        :rtype: recordset
        """
        audit = self._create_general_audit_for_posture(suffix)
        if need_previous:
            audit.need_previous = True
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_b555edd"
        )
        return self.env["general_audit_ws_b555edd"].create(
            {"general_audit_id": audit.id, "type_id": ws_type.id}
        )

    def _equity_source(self):
        """Build a fake ``_get_equity_source`` result.

        Retained earnings opens at 500 and closes at 480 before profit;
        profit is 100 and OCI is 10.

        :return: the dict ``_get_equity_source`` would return
        :rtype: dict
        """
        retained = self.env.ref(
            "ssi_general_audit_worksheet_draft_reporting."
            "general_audit_ws_b555edd_equity_component_retained_earnings"
        )
        return {
            "profit": 100.0,
            "oci": 10.0,
            "components": {retained.id: (500.0, 480.0)},
        }

    def test_equity_reload_allocates_profit_and_oci(self):
        """Reload gives profit to retained earnings and OCI to the OCI line.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        trial balance behind ``_get_equity_source`` is replaced by a
        fixed result). Every line must add up, so no other movement is
        left unexplained.

        :return: nothing; asserts the retained earnings and OCI lines
        """
        worksheet = self._create_b555edd_worksheet("EquityAlloc")
        with mock.patch.object(
            type(worksheet), "_get_equity_source", return_value=self._equity_source()
        ):
            worksheet.action_reload_account()

        lines = worksheet.equity_line_ids
        retained = lines.filtered(lambda r: r.component_id.receive_profit)
        oci = lines.filtered(lambda r: r.component_id.receive_oci)
        self.assertEqual(len(retained), 1)
        self.assertEqual(retained.profit, 100.0)
        self.assertEqual(retained.closing_balance, 580.0)
        self.assertEqual(retained.other_movement, -20.0)
        self.assertEqual(oci.oci, 10.0)
        self.assertEqual(oci.closing_balance, 10.0)
        self.assertEqual(oci.other_movement, 0.0)
        self.assertEqual(sum(lines.mapped("profit")), 100.0)

    def test_equity_owner_transaction_explains_other_movement(self):
        """A typed-in dividend removes the matching other movement.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        source figures are fixed). Retained earnings leaves 20 of
        movement unexplained; a dividend of -20 explains it, and Reload
        again throws the typed-in value away.

        :return: nothing; asserts other movement and the manual flag
        """
        worksheet = self._create_b555edd_worksheet("EquityDividend")
        with mock.patch.object(
            type(worksheet), "_get_equity_source", return_value=self._equity_source()
        ):
            worksheet.action_reload_account()
            retained = worksheet.equity_line_ids.filtered(
                lambda r: r.component_id.receive_profit
            )
            retained.dividend = -20.0

            self.assertEqual(retained.other_movement, 0.0)
            self.assertTrue(worksheet.equity_has_manual)

            worksheet.action_reload_account()

        retained = worksheet.equity_line_ids.filtered(
            lambda r: r.component_id.receive_profit
        )
        self.assertEqual(retained.dividend, 0.0)
        self.assertEqual(retained.other_movement, -20.0)
        self.assertFalse(worksheet.equity_has_manual)

    def test_equity_previous_period_lines_follow_need_previous(self):
        """Previous period lines exist only when the audit keeps one.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        source figures are fixed). The same source is used for both
        periods, so the check is about the line count only.

        :return: nothing; asserts the line count per period
        """
        components = self.env["general_audit_ws_b555edd.equity_component"].search_count(
            []
        )
        without = self._create_b555edd_worksheet("EquityNoPrev")
        with_previous = self._create_b555edd_worksheet("EquityPrev", need_previous=True)
        for worksheet in (without, with_previous):
            with mock.patch.object(
                type(worksheet),
                "_get_equity_source",
                return_value=self._equity_source(),
            ):
                worksheet.action_reload_account()

        self.assertEqual(len(without.equity_current_ids), components)
        self.assertEqual(len(without.equity_previous_ids), 0)
        self.assertEqual(len(with_previous.equity_current_ids), components)
        self.assertEqual(len(with_previous.equity_previous_ids), components)

    def test_equity_reload_without_standard_details(self):
        """Reload on an audit without standard details gives empty lines.

        Pure Python -- trigger P6 (L-15: the real ``_get_equity_source``
        is called inside a test that also patches nothing else, so the
        fixture must be built programmatically). No account type means
        every figure is zero and nothing raises.

        :return: nothing; asserts zero figures on every line
        """
        worksheet = self._create_b555edd_worksheet("EquityEmpty")

        worksheet.action_reload_account()

        lines = worksheet.equity_line_ids
        self.assertTrue(lines)
        self.assertFalse(any(lines.mapped("closing_balance")))
        self.assertFalse(any(lines.mapped("other_movement")))
