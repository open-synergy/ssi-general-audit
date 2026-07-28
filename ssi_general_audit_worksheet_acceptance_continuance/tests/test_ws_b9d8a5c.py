# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from datetime import date

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestGeneralAuditWsb9d8a5c(YamlTransactionCase):
    def test_general_audit_ws_b9d8a5c(self):
        """Run the declarative YAML scenarios for worksheet b9d8a5c."""
        self.run_yaml_scenario("test_data_ws_b9d8a5c.yaml")

    # ------------------------------------------------------------------
    # Shared fixture builder for the Python-only tests below.
    # ------------------------------------------------------------------
    def _create_worksheet(self):
        """Build a minimal, opened ``general_audit`` and its
        ``general_audit_ws_b9d8a5c`` worksheet.

        Used as fixture for the Python-only tests in this class (see each
        test's docstring for the `odoo-yaml-test` limitation code that
        forces it out of YAML).

        :return: a ``general_audit_ws_b9d8a5c`` record
        """
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        partner = (
            self.env["res.partner"]
            .sudo()
            .create({"name": "Test Dedup Client", "is_company": True})
        )
        accountant = (
            self.env["res.partner"].sudo().create({"name": "Test Dedup Accountant"})
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].sudo().create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-B9D8A5C-%s" % accountant.id,
            }
        )
        account_type_set = (
            self.env["client_account_type_set"]
            .sudo()
            .create({"name": "Test Dedup Account Type Set", "code": "/"})
        )
        standard = (
            self.env["accountant.financial_accounting_standard"]
            .sudo()
            .create({"name": "Test Dedup Standard", "code": "/"})
        )
        audit = (
            self.env["general_audit"]
            .sudo()
            .create(
                {
                    "title": "Test General Audit - WS b9d8a5c Python",
                    "partner_id": partner.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": account_type_set.id,
                    "financial_accounting_standard_id": standard.id,
                    "date_start": date(2026, 1, 1),
                    "date_end": date(2026, 12, 31),
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        audit.action_open()
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_acceptance_continuance."
            "worksheet_type_b9d8a5c"
        )
        return (
            self.env["general_audit_ws_b9d8a5c"]
            .sudo()
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )

    def _drop_unique_constraint(self, model_name):
        """Temporarily drop the ``unique_worksheet_employee`` constraint.

        Only valid for the remainder of the current test's transaction --
        `TransactionCase` rolls back to a savepoint after every test
        method, including DDL changes, so the constraint is intact again
        for subsequent tests.

        :param str model_name: technical model name whose
            ``_sql_constraints`` unique constraint should be dropped.
        :return: None
        """
        table = self.env[model_name]._table
        self.env.cr.execute(
            "SELECT conname FROM pg_constraint "
            "WHERE conrelid = %s::regclass AND contype = 'u' "
            "AND conname LIKE %s",
            (table, "%unique_worksheet_employee%"),
        )
        row = self.env.cr.fetchone()
        self.assertTrue(
            row, "unique_worksheet_employee constraint not found on %s" % table
        )
        self.env.cr.execute('ALTER TABLE "%s" DROP CONSTRAINT "%s"' % (table, row[0]))

    # ------------------------------------------------------------------
    # De-duplication of pre-existing duplicate rows (issue #110 core fix)
    # ------------------------------------------------------------------
    def test_action_create_summary_deduplicates_existing_rows(self):
        """Python murni -- pemicu P10 (L-09..L-11: fixture butuh Python
        sungguhan) dan P5 (L-22: `_sql_constraints` UNIQUE
        `(worksheet_id, employee_id)` memblokir pembuatan baris kembar
        lewat ORM, sehingga fixture duplikat harus dibuat lewat SQL
        mentah dengan constraint dilepas sementara -- tidak bisa ditulis
        di YAML sama sekali).

        Meniru kondisi WS 75 (tiket helpdesk HT/26/000574): dua baris
        `.competency`/`.availability`/`.independency`/`.summary` untuk
        `employee_id` yang sama pada satu worksheet, seperti yang bisa
        terjadi sebelum constraint UNIQUE ada. Setelah
        `action_create_summary()` dijalankan, tiap tabel harus
        menyisakan tepat satu baris per employee -- baris ber-``id``
        terkecil yang dipertahankan.
        """
        worksheet = self._create_worksheet()
        job = self.env["hr.job"].sudo().create({"name": "Audit Senior - dedup"})
        employee = (
            self.env["hr.employee"]
            .sudo()
            .create(
                {
                    "name": "Test Auditor Dedup",
                    "job_id": job.id,
                    "audit_ok": True,
                }
            )
        )
        self.env["general_audit_ws_b9d8a5c.personnel"].sudo().create(
            {
                "worksheet_id": worksheet.id,
                "employee_id": employee.id,
                "job_id": job.id,
                "proposed": "yes",
            }
        )

        models_to_dup = [
            "general_audit_ws_b9d8a5c.competency",
            "general_audit_ws_b9d8a5c.availability",
            "general_audit_ws_b9d8a5c.independency",
            "general_audit_ws_b9d8a5c.summary",
        ]
        kept_ids = {}
        for model_name in models_to_dup:
            Model = self.env[model_name].sudo()
            first = Model.create(
                {"worksheet_id": worksheet.id, "employee_id": employee.id}
            )
            kept_ids[model_name] = first.id
            self._drop_unique_constraint(model_name)
            Model.create({"worksheet_id": worksheet.id, "employee_id": employee.id})
            # Sanity check: the fixture really has 2 rows before de-dup.
            self.assertEqual(
                Model.search_count(
                    [
                        ("worksheet_id", "=", worksheet.id),
                        ("employee_id", "=", employee.id),
                    ]
                ),
                2,
            )

        worksheet.action_create_summary()

        for model_name in models_to_dup:
            remaining = (
                self.env[model_name]
                .sudo()
                .search(
                    [
                        ("worksheet_id", "=", worksheet.id),
                        ("employee_id", "=", employee.id),
                    ]
                )
            )
            self.assertEqual(
                len(remaining),
                1,
                "%s must keep exactly one row after de-duplication" % model_name,
            )
            self.assertEqual(
                remaining.id,
                kept_ids[model_name],
                "%s must keep the row with the smallest id" % model_name,
            )

    # ------------------------------------------------------------------
    # _sql_constraints UNIQUE(worksheet_id, employee_id)
    # ------------------------------------------------------------------
    @mute_logger("odoo.sql_db")
    def test_personnel_unique_worksheet_employee_constraint(self):
        """Python murni -- pemicu P5 (L-22: `psycopg2.IntegrityError` di
        luar 12 tipe yang dikenali `expect_error`, dipicu `_sql_constraints`
        UNIQUE `(worksheet_id, employee_id)` pada
        ``general_audit_ws_b9d8a5c.personnel``).

        Membuat baris personel kedua dengan `worksheet_id` + `employee_id`
        yang sama harus ditolak basis data.
        """
        worksheet = self._create_worksheet()
        job = self.env["hr.job"].sudo().create({"name": "Audit Senior - personnel"})
        employee = (
            self.env["hr.employee"]
            .sudo()
            .create(
                {
                    "name": "Test Auditor Personnel Unique",
                    "job_id": job.id,
                    "audit_ok": True,
                }
            )
        )
        Personnel = self.env["general_audit_ws_b9d8a5c.personnel"].sudo()
        Personnel.create(
            {
                "worksheet_id": worksheet.id,
                "employee_id": employee.id,
                "job_id": job.id,
            }
        )
        with self.assertRaises(IntegrityError):
            Personnel.create(
                {
                    "worksheet_id": worksheet.id,
                    "employee_id": employee.id,
                    "job_id": job.id,
                }
            )

    @mute_logger("odoo.sql_db")
    def test_summary_unique_worksheet_employee_constraint(self):
        """Python murni -- pemicu P5 (L-22: `psycopg2.IntegrityError` di
        luar 12 tipe yang dikenali `expect_error`, dipicu `_sql_constraints`
        UNIQUE `(worksheet_id, employee_id)` pada
        ``general_audit_ws_b9d8a5c.summary``).

        Membuat baris summary kedua dengan `worksheet_id` + `employee_id`
        yang sama harus ditolak basis data.
        """
        worksheet = self._create_worksheet()
        job = self.env["hr.job"].sudo().create({"name": "Audit Senior - summary"})
        employee = (
            self.env["hr.employee"]
            .sudo()
            .create(
                {
                    "name": "Test Auditor Summary Unique",
                    "job_id": job.id,
                    "audit_ok": True,
                }
            )
        )
        Summary = self.env["general_audit_ws_b9d8a5c.summary"].sudo()
        Summary.create({"worksheet_id": worksheet.id, "employee_id": employee.id})
        with self.assertRaises(IntegrityError):
            Summary.create({"worksheet_id": worksheet.id, "employee_id": employee.id})
