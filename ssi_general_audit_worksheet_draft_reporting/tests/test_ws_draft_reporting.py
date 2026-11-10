# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from types import SimpleNamespace
from unittest import mock

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


class _FakeDetail(SimpleNamespace):
    """Stand-in for a ``general_audit.standard_detail`` row.

    Gives ``detail[field]`` access on top of attribute access, as the
    cash flow computation reads balances by field name.
    """

    def __getitem__(self, key):
        """Return the attribute called ``key``.

        :param str key: name of the balance field
        :return: its value
        """
        return getattr(self, key)


class _FakeRows(list):
    """List of stand-in rows that also answers ``mapped`` and ``filtered``."""

    def mapped(self, name):
        """Return the attribute ``name`` of every row.

        :param str name: attribute to read
        :return: one value per row
        :rtype: list
        """
        return [getattr(row, name) for row in self]

    def filtered(self, func):
        """Keep the rows for which ``func`` is true.

        :param func: predicate applied to each row
        :return: the matching rows
        :rtype: _FakeRows
        """
        return _FakeRows(row for row in self if func(row))


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
        again keeps both the typed-in value and the line itself.

        :return: nothing; asserts other movement and the line identity
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

            worksheet.action_reload_account()

        kept = worksheet.equity_line_ids.filtered(
            lambda r: r.component_id.receive_profit
        )
        self.assertEqual(kept, retained)
        self.assertEqual(kept.dividend, -20.0)
        self.assertEqual(kept.other_movement, 0.0)

    def test_equity_reload_keeps_owner_transactions_and_follows_source(self):
        """Reload refreshes the source columns and spares the typed ones.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        source figures are fixed and then changed). All four owner
        transactions are typed in, the source profit moves from 100 to
        150, and Reload must follow the source without touching the
        typed-in values or the id of the line.

        :return: nothing; asserts source and typed-in columns
        """
        worksheet = self._create_b555edd_worksheet("EquityKeep")
        with mock.patch.object(
            type(worksheet), "_get_equity_source", return_value=self._equity_source()
        ):
            worksheet.action_reload_account()
        retained = worksheet.equity_line_ids.filtered(
            lambda r: r.component_id.receive_profit
        )
        retained.write(
            {"issuance": 1.0, "treasury": -2.0, "reserve": 3.0, "dividend": -4.0}
        )
        source = self._equity_source()
        source["profit"] = 150.0
        with mock.patch.object(
            type(worksheet), "_get_equity_source", return_value=source
        ):
            worksheet.action_reload_account()

        kept = worksheet.equity_line_ids.filtered(
            lambda r: r.component_id.receive_profit
        )
        self.assertEqual(kept, retained)
        self.assertEqual(kept.profit, 150.0)
        self.assertEqual(kept.closing_balance, 630.0)
        self.assertEqual(
            (kept.issuance, kept.treasury, kept.reserve, kept.dividend),
            (1.0, -2.0, 3.0, -4.0),
        )
        self.assertEqual(kept.other_movement, -18.0)

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

    def test_equity_previous_lines_follow_need_previous_toggle(self):
        """Switching ``need_previous`` adds or drops only the previous lines.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        source figures are fixed). Turning the flag on creates the
        previous period lines and leaves the current ones alone; turning
        it off removes only the previous ones.

        :return: nothing; asserts the lines and their ids per period
        """
        worksheet = self._create_b555edd_worksheet("EquityToggle")
        with mock.patch.object(
            type(worksheet), "_get_equity_source", return_value=self._equity_source()
        ):
            worksheet.action_reload_account()
            current = worksheet.equity_current_ids
            self.assertFalse(worksheet.equity_previous_ids)

            worksheet.general_audit_id.need_previous = True
            worksheet.action_reload_account()
            self.assertEqual(worksheet.equity_current_ids, current)
            self.assertEqual(len(worksheet.equity_previous_ids), len(current))

            worksheet.general_audit_id.need_previous = False
            worksheet.action_reload_account()
            self.assertEqual(worksheet.equity_current_ids, current)
            self.assertFalse(worksheet.equity_previous_ids)

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

    def _fake_lead_schedule(self, details, receivers=None, amounts=None):
        """Build a stand-in for a ``general_audit_ws_b26d482`` record.

        :param list details: ``(account type, normal balance, balance
            sheet amount)`` tuples, one per Worksheet line
        :param dict receivers: receiving accounts by destination type id
        :param dict amounts: closing amounts by destination type id
        :return: object giving ``detail_ids`` and
            ``_get_closing_allocation()``
        :rtype: SimpleNamespace
        """
        lines = [
            SimpleNamespace(
                account_id=SimpleNamespace(type_id=type_, normal_balance=normal),
                balance_sheet=amount,
            )
            for type_, normal, amount in details
        ]
        return SimpleNamespace(
            detail_ids=lines,
            _get_closing_allocation=lambda: (receivers or {}, amounts or {}),
        )

    def _reload_with_lead_schedule(self, worksheet, fake):
        """Reload ``worksheet`` while the Worksheet source is ``fake``.

        :param recordset worksheet: the ``general_audit_ws_b555edd``
        :param fake: result of ``_fake_lead_schedule``
        :return: the current period equity lines by component
        :rtype: dict
        """
        with mock.patch.object(
            type(worksheet), "_get_lead_schedule_worksheet", return_value=fake
        ):
            worksheet.action_reload_account()
        lines = worksheet.equity_line_ids.filtered(lambda r: r.period == "current")
        return {line.component_id: line for line in lines}

    def test_equity_closing_comes_from_lead_schedule_worksheet(self):
        """The closing balance is the Balance Sheet of the Worksheet lines.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        Worksheet is replaced by a fixed stand-in). The retained
        earnings line reads 580 from the Worksheet, not the standard
        detail balance plus profit and OCI.

        :return: nothing; asserts the retained earnings closing balance
        """
        retained = self.env["general_audit_ws_b555edd.equity_component"].search(
            [("receive_profit", "=", True)], limit=1
        )
        fake = self._fake_lead_schedule([(retained.type_ids[:1], "cr", 580.0)])
        worksheet = self._create_b555edd_worksheet("EquityFromWorksheet")

        lines = self._reload_with_lead_schedule(worksheet, fake)

        self.assertEqual(lines[retained].closing_balance, 580.0)
        self.assertEqual(lines[retained].other_movement, 580.0)

    def test_equity_closing_counts_debit_normal_type_negative(self):
        """A debit-normal account reduces the equity of its component.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). The
        Worksheet shows 30 on the debit side, which is -30 of equity.

        :return: nothing; asserts the sign of the closing balance
        """
        component = self.env["general_audit_ws_b555edd.equity_component"].search(
            [("receive_profit", "=", True)], limit=1
        )
        fake = self._fake_lead_schedule([(component.type_ids[:1], "dr", 30.0)])
        worksheet = self._create_b555edd_worksheet("EquityDebitNormal")

        lines = self._reload_with_lead_schedule(worksheet, fake)

        self.assertEqual(lines[component].closing_balance, -30.0)

    def test_equity_closing_includes_type_without_receiving_account(self):
        """Closing to a type that no account receives still reaches equity.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). The
        OCI type has a closing amount of 10 and no receiving account,
        so the OCI component carries it, positive on a credit-normal
        type.

        :return: nothing; asserts the OCI closing balance
        """
        component = self.env["general_audit_ws_b555edd.equity_component"].search(
            [("receive_oci", "=", True)], limit=1
        )
        type_ = component.type_ids[:1]
        fake = self._fake_lead_schedule([], amounts={type_.id: 10.0})
        worksheet = self._create_b555edd_worksheet("EquityNoReceiver")

        lines = self._reload_with_lead_schedule(worksheet, fake)

        sign = 1 if type_.normal_balance == "cr" else -1
        self.assertEqual(lines[component].closing_balance, sign * 10.0)

    def test_equity_closing_skips_type_with_receiving_account(self):
        """A closing that an account receives is not counted twice.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). The
        receiving account already holds the closing in its Balance
        Sheet column, so the type amount adds nothing on top.

        :return: nothing; asserts the OCI closing balance stays zero
        """
        component = self.env["general_audit_ws_b555edd.equity_component"].search(
            [("receive_oci", "=", True)], limit=1
        )
        type_ = component.type_ids[:1]
        fake = self._fake_lead_schedule(
            [], receivers={type_.id: object()}, amounts={type_.id: 10.0}
        )
        worksheet = self._create_b555edd_worksheet("EquityWithReceiver")

        lines = self._reload_with_lead_schedule(worksheet, fake)

        self.assertEqual(lines[component].closing_balance, 0.0)

    def test_equity_previous_period_ignores_lead_schedule_worksheet(self):
        """Only the current period reads the Worksheet.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). The
        Worksheet has no previous period, so the previous lines keep
        the standard detail balance, zero on this empty audit.

        :return: nothing; asserts the previous closing balances are zero
        """
        retained = self.env["general_audit_ws_b555edd.equity_component"].search(
            [("receive_profit", "=", True)], limit=1
        )
        fake = self._fake_lead_schedule([(retained.type_ids[:1], "cr", 580.0)])
        worksheet = self._create_b555edd_worksheet("EquityPrevious", True)

        self._reload_with_lead_schedule(worksheet, fake)

        previous = worksheet.equity_line_ids.filtered(lambda r: r.period == "previous")
        self.assertTrue(previous)
        self.assertFalse(any(previous.mapped("closing_balance")))

    def test_lead_schedule_worksheet_without_detail_is_ignored(self):
        """A Worksheet without lines is not used as the source.

        Pure Python -- trigger P1 (L-01: the return value of the
        method is what is asserted). The audit has a Worksheet with no
        detail lines, so there is nothing to read from.

        :return: nothing; asserts no Worksheet is found
        """
        worksheet = self._create_b555edd_worksheet("EquityEmptyWorksheet")
        self.env["general_audit_ws_b26d482"].create(
            {
                "general_audit_id": worksheet.general_audit_id.id,
                "type_id": self.env.ref(
                    "ssi_general_audit_worksheet_lead_schedule.worksheet_type_b26d482"
                ).id,
            }
        )

        self.assertFalse(worksheet._get_lead_schedule_worksheet())

    _CF_PREFIX = (
        "ssi_general_audit_worksheet_draft_reporting."
        "general_audit_ws_b555edd_cashflow_item_"
    )

    def _cf_item(self, key):
        """Return a seeded cash flow item by the end of its XML ID.

        :param str key: for example ``ar`` or ``capex``
        :return: the ``general_audit_ws_b555edd.cashflow_item`` record
        :rtype: recordset
        """
        return self.env.ref(self._CF_PREFIX + key)

    def _cf_lines(self, worksheet, period="current"):
        """Map the cash flow lines of a period by the item XML ID suffix.

        :param recordset worksheet: the ``general_audit_ws_b555edd``
        :param str period: ``current`` or ``previous``
        :return: ``{"ar": line, ...}``
        :rtype: dict
        """
        lines = worksheet.cashflow_line_ids.filtered(lambda r: r.period == period)
        result = {}
        for line in lines:
            xml = self.env["ir.model.data"].search(
                [
                    ("model", "=", "general_audit_ws_b555edd.cashflow_item"),
                    ("res_id", "=", line.item_id.id),
                ],
                limit=1,
            )
            result[xml.name[len("general_audit_ws_b555edd_cashflow_item_") :]] = line
        return result

    def _cf_reload(self, worksheet, amounts):
        """Reload ``worksheet`` with a fixed cash flow source.

        :param recordset worksheet: the ``general_audit_ws_b555edd``
        :param dict amounts: ``{item XML ID suffix: amount}``
        :return: the current period lines, see ``_cf_lines``
        :rtype: dict
        """
        source = {self._cf_item(key).id: value for key, value in amounts.items()}
        with mock.patch.object(
            type(worksheet), "_get_cashflow_source", return_value=source
        ):
            worksheet.action_reload_account()
        return self._cf_lines(worksheet)

    def test_cashflow_amounts_follow_balance_sides(self):
        """Balance changes are cash flows by the normal balance side.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        standard details are stand-ins carrying chosen balances, since a
        real trial balance for every account type is too heavy to build).
        Receivables rise by 100 (outflow), payables rise by 40 (inflow),
        fixed assets rise by 50 with 30 depreciation (outflow of 80),
        and interest expense of 20 is added back then paid.

        :return: nothing; asserts the computed amounts
        """
        worksheet = self._create_b555edd_worksheet("CashflowAmounts")

        def detail(xml_id, opening, closing):
            """Build a stand-in standard detail for an account type."""
            return _FakeDetail(
                type_id=self.env.ref("ssi_general_audit." + xml_id),
                home_statement_opening_balance=opening,
                audited_balance=closing,
                previous_opening_balance=0.0,
                previous_balance=0.0,
            )

        details = [
            detail("client_account_type_2_4fbd7be2", 100.0, 200.0),
            detail("client_account_type_19_17733e6d", 50.0, 90.0),
            detail("client_account_type_14_e160db3b", 1000.0, 1050.0),
            detail("client_account_type_53_88b4482b", 0.0, 30.0),
            detail("client_account_type_54_c3a5a82b", 0.0, 20.0),
            detail("client_account_type_1_e046f813", 300.0, 400.0),
        ]
        items = self.env["general_audit_ws_b555edd.cashflow_item"].search([])

        amounts = worksheet._compute_cashflow_amounts(items, details, "current")

        def amount(key):
            """Return the computed amount of a seeded item."""
            return amounts[self._cf_item(key).id]

        self.assertEqual(amount("ar"), -100.0)
        self.assertEqual(amount("ap"), 40.0)
        self.assertEqual(amount("capex"), -80.0)
        self.assertEqual(amount("interest_expense"), 20.0)
        self.assertEqual(amount("interest_paid"), -20.0)
        self.assertEqual(amount("depreciation"), 30.0)
        self.assertEqual(amount("cash_opening"), 300.0)
        self.assertEqual(amount("cash_closing_tb"), 400.0)

    def test_cashflow_totals_and_cash_difference(self):
        """Summary lines add up and a typed-in amount refreshes them.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        calculated amounts are fixed). Operating -60, investing -80 and
        financing +20 give a net change of -120, so opening cash 300
        becomes 180 against 280 in the trial balance (difference -100).
        Typing dividends paid of -10 moves the difference to -110.

        :return: nothing; asserts the summary lines before and after
        """
        worksheet = self._create_b555edd_worksheet("CashflowTotals")
        lines = self._cf_reload(
            worksheet,
            {
                "ar": -100.0,
                "ap": 40.0,
                "capex": -80.0,
                "share_capital": 20.0,
                "cash_opening": 300.0,
                "cash_closing_tb": 280.0,
            },
        )

        self.assertEqual(lines["operating_total"].amount, -60.0)
        self.assertEqual(lines["investing_total"].amount, -80.0)
        self.assertEqual(lines["financing_total"].amount, 20.0)
        self.assertEqual(lines["net_change"].amount, -120.0)
        self.assertEqual(lines["cash_closing_computed"].amount, 180.0)
        self.assertEqual(lines["cash_difference"].amount, -100.0)

        lines["dividend_paid"].amount = -10.0

        lines = self._cf_lines(worksheet)
        self.assertEqual(lines["financing_total"].amount, 10.0)
        self.assertEqual(lines["cash_difference"].amount, -110.0)

    def test_cashflow_new_manual_rows_feed_totals(self):
        """Typed-in auditor rows move the totals and the closing cash.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        calculated amounts are fixed). Operating -60, investing -80 and
        financing +20 give a net change of -120 and, with opening cash
        300, a computed closing cash of 180. A non-cash adjustment of
        25 lifts operating to -35, other investing of -15 lowers
        investing to -95, and the exchange rate effect of 7 is added to
        the closing cash without entering the net change. The three
        seeded items carry the agreed section, calculation and order.
        Reload again keeps the three typed-in amounts and the line ids.

        :return: nothing; asserts the seed and the summary lines
        """
        noncash = self._cf_item("noncash_adjustment")
        other_investing = self._cf_item("other_investing")
        fx_item = self._cf_item("fx_effect")
        self.assertEqual(
            (noncash.section, noncash.calc_type, noncash.sequence),
            ("operating_adjustment", "manual", 55),
        )
        self.assertEqual(
            (other_investing.section, other_investing.calc_type),
            ("investing", "manual"),
        )
        self.assertEqual(other_investing.sequence, 275)
        self.assertEqual(
            (fx_item.section, fx_item.calc_type, fx_item.sequence),
            ("summary", "fx_effect", 385),
        )

        worksheet = self._create_b555edd_worksheet("CashflowNewRows")
        source = {
            "ar": -100.0,
            "ap": 40.0,
            "capex": -80.0,
            "share_capital": 20.0,
            "cash_opening": 300.0,
            "cash_closing_tb": 280.0,
        }
        lines = self._cf_reload(worksheet, source)
        self.assertEqual(lines["fx_effect"].amount, 0.0)
        self.assertEqual(lines["cash_closing_computed"].amount, 180.0)

        lines["noncash_adjustment"].amount = 25.0
        lines["other_investing"].amount = -15.0
        lines["fx_effect"].amount = 7.0

        lines = self._cf_lines(worksheet)
        self.assertEqual(lines["operating_total"].amount, -35.0)
        self.assertEqual(lines["investing_total"].amount, -95.0)
        self.assertEqual(lines["net_change"].amount, -110.0)
        self.assertEqual(lines["cash_closing_computed"].amount, 197.0)
        self.assertEqual(lines["cash_difference"].amount, -83.0)

        kept_ids = {key: line.id for key, line in lines.items()}
        lines = self._cf_reload(worksheet, source)
        self.assertEqual({key: line.id for key, line in lines.items()}, kept_ids)
        self.assertEqual(lines["noncash_adjustment"].amount, 25.0)
        self.assertEqual(lines["other_investing"].amount, -15.0)
        self.assertEqual(lines["fx_effect"].amount, 7.0)
        self.assertEqual(lines["operating_total"].amount, -35.0)
        self.assertEqual(lines["cash_closing_computed"].amount, 197.0)
        self.assertEqual(lines["cash_difference"].amount, -83.0)

    def test_cashflow_reload_keeps_manual_amounts(self):
        """Reload keeps the typed-in amounts and follows the source.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        calculated amounts are fixed and then changed). A dividend paid
        typed in survives the next Reload with the same line id, while
        the calculated receivables line follows the new source.

        :return: nothing; asserts the manual and the calculated line
        """
        worksheet = self._create_b555edd_worksheet("CashflowReload")
        lines = self._cf_reload(worksheet, {"ar": -100.0})
        lines["dividend_paid"].amount = -10.0
        manual_id = lines["dividend_paid"].id

        lines = self._cf_reload(worksheet, {"ar": -150.0})

        self.assertEqual(lines["dividend_paid"].id, manual_id)
        self.assertEqual(lines["dividend_paid"].amount, -10.0)
        self.assertEqual(lines["ar"].amount, -150.0)

    def test_cashflow_previous_lines_follow_need_previous_toggle(self):
        """Switching ``need_previous`` adds or drops only the previous lines.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        calculated amounts are fixed). A manual amount typed on the
        current period survives both switches.

        :return: nothing; asserts the lines per period
        """
        worksheet = self._create_b555edd_worksheet("CashflowToggle")
        lines = self._cf_reload(worksheet, {"ar": -100.0})
        lines["dividend_paid"].amount = -10.0
        current = worksheet.cashflow_current_ids
        self.assertFalse(worksheet.cashflow_previous_ids)

        worksheet.general_audit_id.need_previous = True
        lines = self._cf_reload(worksheet, {"ar": -100.0})
        self.assertEqual(worksheet.cashflow_current_ids, current)
        self.assertEqual(len(worksheet.cashflow_previous_ids), len(current))
        self.assertEqual(lines["dividend_paid"].amount, -10.0)

        worksheet.general_audit_id.need_previous = False
        lines = self._cf_reload(worksheet, {"ar": -100.0})
        self.assertEqual(worksheet.cashflow_current_ids, current)
        self.assertFalse(worksheet.cashflow_previous_ids)
        self.assertEqual(lines["dividend_paid"].amount, -10.0)

    def test_detail_reload_follows_standard_details(self):
        """Reload adds new standard details and drops the vanished ones.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        standard details the audit exposes are replaced by a fixed set,
        because ``standard_detail_id`` is ``ondelete="restrict"`` and a
        real standard detail cannot be deleted while a line uses it). A
        new standard detail adds one line and leaves the others
        untouched; a standard detail that vanishes removes only its own
        line.

        :return: nothing; asserts the detail lines and their ids
        """
        worksheet = self._create_b555edd_worksheet("DetailSync")
        audit = worksheet.general_audit_id
        types = self.env["client_account_type"].search([], limit=3)
        standard_model = self.env["general_audit.standard_detail"]
        first = standard_model.create(
            {"general_audit_id": audit.id, "type_id": types[0].id}
        )
        standard_model.create({"general_audit_id": audit.id, "type_id": types[1].id})
        worksheet.action_reload_account()
        old_lines = worksheet.detail_ids
        self.assertEqual(len(old_lines), 2)

        third = standard_model.create(
            {"general_audit_id": audit.id, "type_id": types[2].id}
        )
        worksheet.action_reload_account()
        self.assertEqual(len(worksheet.detail_ids), 3)
        self.assertEqual(worksheet.detail_ids & old_lines, old_lines)

        first_line = old_lines.filtered(lambda r: r.standard_detail_id == first)
        with mock.patch.object(
            type(audit),
            "standard_detail_ids",
            new_callable=mock.PropertyMock,
            return_value=first | third,
        ):
            worksheet.action_reload_account()
        self.assertEqual(
            worksheet.detail_ids.mapped("standard_detail_id"), first | third
        )
        self.assertEqual(worksheet.detail_ids & old_lines, first_line)

    def test_cashflow_previous_period_lines_follow_need_previous(self):
        """Previous period cash flow lines exist only when kept.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        calculated amounts are fixed). The same source serves both
        periods, so only the line count is checked.

        :return: nothing; asserts the line count per period
        """
        items = self.env["general_audit_ws_b555edd.cashflow_item"].search_count([])
        without = self._create_b555edd_worksheet("CashflowNoPrev")
        with_previous = self._create_b555edd_worksheet(
            "CashflowPrev", need_previous=True
        )
        for worksheet in (without, with_previous):
            self._cf_reload(worksheet, {"ar": -100.0})

        self.assertEqual(len(without.cashflow_current_ids), items)
        self.assertEqual(len(without.cashflow_previous_ids), 0)
        self.assertEqual(len(with_previous.cashflow_previous_ids), items)

    def test_cashflow_reload_without_standard_details(self):
        """Reload on an audit without standard details gives zero lines.

        Pure Python -- trigger P1 (L-01: the fixture is built
        programmatically and the amounts of every line are read back).
        No account type means every amount and the cash difference are
        zero, and nothing raises.

        :return: nothing; asserts zero amounts on every line
        """
        worksheet = self._create_b555edd_worksheet("CashflowEmpty")

        worksheet.action_reload_account()

        lines = worksheet.cashflow_line_ids
        self.assertTrue(lines)
        self.assertFalse(any(lines.mapped("amount")))

    def _create_balance_detail(self, worksheet, type_, current, previous):
        """Create a standard detail and its b555edd line with balances.

        :param recordset worksheet: the b555edd worksheet
        :param recordset type_: the ``client_account_type`` of the line
        :param float current: audited balance of the current period
        :param float previous: balance of the previous period
        :return: the ``general_audit_ws_b555edd.detail`` record
        :rtype: recordset
        """
        standard = self.env["general_audit.standard_detail"].create(
            {"general_audit_id": worksheet.general_audit_id.id, "type_id": type_.id}
        )
        standard.write({"audited_balance": current, "previous_balance": previous})
        return self.env["general_audit_ws_b555edd.detail"].create(
            {"worksheet_id": worksheet.id, "standard_detail_id": standard.id}
        )

    def _profit_by_field(self, total_type, field, details):
        """Fake ``_get_formula_total``: profit 100 now, 40 before.

        :param str total_type: ``total_type`` asked for
        :param str field: balance field asked for
        :param details: ignored
        :return: the fixed profit of the period
        :rtype: float
        """
        if total_type != "profit_after_tax":
            return 0.0
        return 100.0 if field == "audited_balance" else 40.0

    def test_retained_earnings_balance_adds_profit(self):
        """Retained earnings line shows audit balance plus period profit.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        profit total is fixed at 100 and 40). The cash line and a
        profit free worksheet must keep the plain audited balance.

        :return: nothing; asserts the balances of both lines
        """
        retained_type = self.env.ref(
            "ssi_general_audit.client_account_type_44_a5c4f192"
        )
        other_type = self.env["client_account_type"].search(
            [("id", "!=", retained_type.id)], limit=1
        )
        worksheet = self._create_b555edd_worksheet("RetainedProfit")
        with mock.patch.object(
            type(worksheet),
            "_get_formula_total",
            side_effect=lambda t, f, d: self._profit_by_field(t, f, d),
        ):
            retained = self._create_balance_detail(worksheet, retained_type, 500, 300)
            other = self._create_balance_detail(worksheet, other_type, 70, 60)
            self.assertEqual(retained.current_balance, 600.0)
            self.assertEqual(retained.previous_balance, 340.0)
            self.assertEqual(other.current_balance, 70.0)
            self.assertEqual(other.previous_balance, 60.0)

    def test_retained_earnings_balance_without_profit(self):
        """Without any profit the retained earnings line is unchanged.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). A
        General Audit without profit and loss balances gives a zero
        ``profit_after_tax`` total.

        :return: nothing; asserts the balances equal the audit balances
        """
        retained_type = self.env.ref(
            "ssi_general_audit.client_account_type_44_a5c4f192"
        )
        worksheet = self._create_b555edd_worksheet("RetainedNoProfit")
        retained = self._create_balance_detail(worksheet, retained_type, 500, 300)
        self.assertEqual(retained.current_balance, 500.0)
        self.assertEqual(retained.previous_balance, 300.0)

    def _create_closing_line(self, worksheet, type_, **amounts):
        """Create a destination closing line on the audit of a worksheet.

        :param worksheet: the ``general_audit_ws_b555edd`` record
        :param recordset type_: destination ``client_account_type``
        :param amounts: ``debit`` and ``credit`` of the line
        :return: the ``general_audit.closing_line`` record
        :rtype: recordset
        """
        return self.env["general_audit.closing_line"].create(
            dict(
                general_audit_id=worksheet.general_audit_id.id,
                name="Test closing line",
                account_type_id=type_.id,
                **amounts,
            )
        )

    def test_closing_is_single_source_for_destination_type(self):
        """Generated closing replaces the profit added to retained earnings.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML; the
        profit total is fixed at 100 and 40). The destination lines
        give 80 - 30 = 50 on the credit-normal retained earnings type:
        the current balance is the audit balance plus 50 and no profit,
        while the previous period still adds its profit.

        :return: nothing; asserts the current and previous balances
        """
        retained_type = self.env.ref(
            "ssi_general_audit.client_account_type_44_a5c4f192"
        )
        worksheet = self._create_b555edd_worksheet("ClosingSingleSource")
        self._create_closing_line(worksheet, retained_type, credit=80.0)
        self._create_closing_line(worksheet, retained_type, debit=30.0)
        with mock.patch.object(
            type(worksheet),
            "_get_formula_total",
            side_effect=lambda t, f, d: self._profit_by_field(t, f, d),
        ):
            retained = self._create_balance_detail(worksheet, retained_type, 500, 300)
            self.assertEqual(retained.current_balance, 550.0)
            self.assertEqual(retained.previous_balance, 340.0)

    def test_closing_to_other_type_skips_profit_on_retained_earnings(self):
        """Closing to another type leaves retained earnings without profit.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). The
        closing lines target a debit-normal type, so that line adds
        ``debit - credit`` and the retained earnings line keeps only
        its audit balance.

        :return: nothing; asserts the balances of both lines
        """
        retained_type = self.env.ref(
            "ssi_general_audit.client_account_type_44_a5c4f192"
        )
        other_type = self.env["client_account_type"].search(
            [("id", "!=", retained_type.id), ("normal_balance", "=", "dr")],
            limit=1,
        )
        worksheet = self._create_b555edd_worksheet("ClosingOtherType")
        self._create_closing_line(worksheet, other_type, debit=40.0)
        self._create_closing_line(worksheet, other_type, credit=10.0)
        with mock.patch.object(
            type(worksheet),
            "_get_formula_total",
            side_effect=lambda t, f, d: self._profit_by_field(t, f, d),
        ):
            retained = self._create_balance_detail(worksheet, retained_type, 500, 300)
            other = self._create_balance_detail(worksheet, other_type, 70, 60)
            self.assertEqual(retained.current_balance, 500.0)
            self.assertEqual(other.current_balance, 100.0)
            self.assertEqual(other.previous_balance, 60.0)

    def test_closing_source_lines_do_not_count(self):
        """Closing lines of closed source accounts change no balance.

        Pure Python -- trigger P6 (L-15: no mock/patch in YAML). A
        closing line with an account is a source line, so the
        retained earnings line keeps the profit it had before.

        :return: nothing; asserts the current balance still adds profit
        """
        retained_type = self.env.ref(
            "ssi_general_audit.client_account_type_44_a5c4f192"
        )
        worksheet = self._create_b555edd_worksheet("ClosingSourceOnly")
        account = self.env["client_account"].create(
            {
                "name": "Test closed source account",
                "code": "ACC-CLOSING-SOURCE",
                "partner_id": worksheet.general_audit_id.partner_id.id,
                "type_id": retained_type.id,
            }
        )
        self.env["general_audit.closing_line"].create(
            {
                "general_audit_id": worksheet.general_audit_id.id,
                "name": "Test source line",
                "account_id": account.id,
                "account_type_id": retained_type.id,
                "debit": 90.0,
            }
        )
        with mock.patch.object(
            type(worksheet),
            "_get_formula_total",
            side_effect=lambda t, f, d: self._profit_by_field(t, f, d),
        ):
            retained = self._create_balance_detail(worksheet, retained_type, 500, 300)
            self.assertEqual(retained.current_balance, 600.0)

    def _fake_posture_worksheet(self, details, closing_lines=None, receivers=None):
        """Build a stand-in Worksheet for the posture Audited column.

        :param list details: ``(group, balance sheet, current profit, oci)``
            tuples, one per Worksheet line
        :param list closing_lines: ``(group, type, debit, credit)`` tuples
            of closing lines without an account
        :param dict receivers: receiving accounts by destination type id
        :return: object giving ``detail_ids``, ``general_audit_id``,
            ``_get_closing_allocation()``, ``net_current_profit`` and
            ``net_oci``
        :rtype: SimpleNamespace
        """
        lines = [
            SimpleNamespace(
                account_id=SimpleNamespace(group_id=group),
                balance_sheet=balance,
                current_profit=profit,
                oci=oci,
            )
            for group, balance, profit, oci in details
        ]
        closing = [
            SimpleNamespace(
                account_id=False,
                account_group_id=group,
                account_type_id=type_,
                debit=debit,
                credit=credit,
            )
            for group, type_, debit, credit in (closing_lines or [])
        ]
        return SimpleNamespace(
            detail_ids=_FakeRows(lines),
            general_audit_id=SimpleNamespace(closing_line_ids=_FakeRows(closing)),
            _get_closing_allocation=lambda: (receivers or {}, {}),
            net_current_profit=1000.0,
            net_oci=-200.0,
        )

    def test_posture_group_audited_comes_from_lead_schedule_worksheet(self):
        """Asset, profit and OCI groups read their own Worksheet column.

        Pure Python -- trigger P1 (L-01: return value of a method) with a
        stand-in Worksheet. Each category reads Balance Sheet, Current
        Profit or OCI respectively.

        :return: nothing; asserts the three amounts
        """
        posture = self.env["general_audit_ws_ff42fdc.posture"]
        groups = self.env["client_account_group"].search([])
        asset = groups.filtered(lambda g: g.report_category == "asset")[:1]
        profit = groups.filtered(lambda g: g.report_category == "profit_loss")[:1]
        oci = groups.filtered(lambda g: g.report_category == "oci")[:1]
        fake = self._fake_posture_worksheet(
            [
                (asset, 700.0, 1.0, 2.0),
                (profit, 3.0, 400.0, 5.0),
                (oci, 6.0, 7.0, -50.0),
            ]
        )
        self.assertEqual(posture._get_lead_schedule_group_amount(fake, asset), 700.0)
        self.assertEqual(posture._get_lead_schedule_group_amount(fake, profit), 400.0)
        self.assertEqual(posture._get_lead_schedule_group_amount(fake, oci), -50.0)

    def test_posture_group_audited_adds_closing_without_receiver(self):
        """Closing of a type without receiving account lands in its group.

        Pure Python -- trigger P1 (L-01). A credit-normal type adds
        credit minus debit; a type with a receiver is skipped, because its
        Balance Sheet already holds it.

        :return: nothing; asserts the group amount
        """
        posture = self.env["general_audit_ws_ff42fdc.posture"]
        group = self.env["client_account_group"].search(
            [("report_category", "=", "equity")], limit=1
        )
        cr_type = SimpleNamespace(id=1, normal_balance="cr")
        received = SimpleNamespace(id=2, normal_balance="cr")
        fake = self._fake_posture_worksheet(
            [(group, 100.0, 0.0, 0.0)],
            closing_lines=[
                (group, cr_type, 10.0, 60.0),
                (group, received, 0.0, 999.0),
            ],
            receivers={2: object()},
        )
        self.assertEqual(posture._get_lead_schedule_group_amount(fake, group), 150.0)

    def test_posture_totals_come_from_lead_schedule_worksheet(self):
        """Profit After Tax and Comprehensive Profit read the net columns.

        Pure Python -- trigger P6 (L-15: mock of the Worksheet search).
        The audited column is the Worksheet net profit, and net profit
        plus net OCI for the comprehensive total.

        :return: nothing; asserts the two totals
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()
        fake = self._fake_posture_worksheet([])
        with mock.patch.object(
            type(worksheet.posture_ids),
            "_get_lead_schedule_worksheet",
            return_value=fake,
        ):
            worksheet.action_load_posture()
            totals = {
                line.total_type: line.audited
                for line in worksheet.posture_ids
                if line.line_type == "total"
            }
        self.assertEqual(totals["profit_after_tax"], 1000.0)
        self.assertEqual(totals["comprehensive_profit"], 800.0)
