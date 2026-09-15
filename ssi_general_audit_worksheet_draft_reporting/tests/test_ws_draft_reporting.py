# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSDraftReporting(YamlTransactionCase):
    """Scenario tests for the ``ssi_general_audit_worksheet_draft_reporting``
    worksheets."""

    # Every ``client_account_group`` code referenced by
    # ``general_audit_ws_ff42fdc._POSTURE_LINE_ORDER`` as a "group" line,
    # mapped to its data XML ID in ``ssi_general_audit``. T006 and T008 are
    # intentionally absent from the layout table, so they are left out here
    # too.
    _GROUP_XML_IDS = {
        "T001": "ssi_general_audit.client_account_group_1_885ef902",
        "T002": "ssi_general_audit.client_account_group_2_becd85c2",
        "T003": "ssi_general_audit.client_account_group_3_8f77474a",
        "T004": "ssi_general_audit.client_account_group_4_8512d9b0",
        "T005": "ssi_general_audit.client_account_group_5_7f3c394c",
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
        covers every "group" entry of ``_POSTURE_LINE_ORDER``. No trial
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
        created Total line) instead of ``_POSTURE_LINE_ORDER`` order,
        because ``Many2one._update_inverses`` (``odoo/fields.py``)
        appends newly created records to the worksheet's already-cached
        ``posture_ids`` tuple instead of re-querying with
        ``_order = "sequence, id"``.

        :return: nothing; asserts count, per-line ``sequence``, and
            that ``posture_ids`` reads back already sorted
        """
        worksheet = self._create_ff42fdc_worksheet_with_all_groups()

        worksheet.action_load_posture()

        order_index = {
            key: position for position, key in enumerate(worksheet._POSTURE_LINE_ORDER)
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
