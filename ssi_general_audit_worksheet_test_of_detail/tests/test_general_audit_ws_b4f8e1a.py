# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import math

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSB4f8e1a(YamlTransactionCase):
    """Cover CRUD and the base workflow for ``general_audit_ws_b4f8e1a``."""

    def test_general_audit_ws_b4f8e1a(self):
        """Run the YAML scenario covering this worksheet."""
        self.run_yaml_scenario("test_data_general_audit_ws_b4f8e1a.yaml")

    def _create_worksheet_fixture(self, population_row_count):
        """Build a minimal general_audit + GL + SD + ToD worksheet fixture,
        entirely through the ORM (no demo data), with a GL population of
        exactly ``population_row_count`` rows.

        :param population_row_count: number of data rows to seed into
            the GL's ``raw_data``, which becomes the linked Sample
            Determination's ``population_count``.
        :return: a ``(worksheet, sample_determination)`` tuple -- the
            opened ``general_audit_ws_b4f8e1a`` record and the linked
            ``general_audit_ws_a916660`` record (write
            ``performance_materiality``/``risk_factor``/
            ``tolerable_misstatement``/``aria`` on the latter, since
            the worksheet's mirrors are read-only).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - B4F8E1A Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - B4F8E1A Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-B4F8E1A-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - B4F8E1A Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - B4F8E1A Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - B4F8E1A Python",
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
            "ssi_general_audit_worksheet_test_of_detail.worksheet_type_b4f8e1a"
        )
        ws_type_d209914 = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        ws_type_a916660 = env.ref(
            "ssi_general_audit_worksheet_sample_determination.worksheet_type_a916660"
        )
        raw_data = "Ref,Amount\n" + "".join(
            "R{0},{0}000\n".format(i) for i in range(1, population_row_count + 1)
        )
        gl = (
            env["general_audit_ws_d209914"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_d209914.id,
                    "raw_data": raw_data,
                }
            )
        )
        sd = (
            env["general_audit_ws_a916660"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_a916660.id,
                    "data_mode": "gl",
                    "general_ledger_id": gl.id,
                }
            )
        )
        worksheet = (
            env["general_audit_ws_b4f8e1a"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type.id,
                    "data_source": "sample",
                    "data_mode": "gl",
                    "general_ledger_id": gl.id,
                    "sample_determination_id": sd.id,
                }
            )
        )
        worksheet.with_user(admin).action_open()
        return worksheet, sd

    def test_precision_interval_chain_matches_formula(self):
        """Pure Python -- trigger P2 (L-04: no float tolerance in YAML
        ``equals``, and ``population_standard_deviation`` /
        ``computed_precision_interval`` / the confidence limits involve
        ``sqrt``, an irrational result that can't be hardcoded as an
        exact YAML expectation).

        Verifies the compute chain (``average_difference`` ->
        ``population_difference_projection`` ->
        ``population_standard_deviation`` ->
        ``computed_precision_interval`` -> upper/lower confidence
        limit) against the same formula applied directly here, per
        HT/26/000689 (``ToD_akun_260821.ods`` cells ``D221``-``D227``).
        """
        worksheet, sd = self._create_worksheet_fixture(population_row_count=10)
        sd.write({"aria": "5"})
        worksheet.write(
            {
                "examination_data": (
                    "Seq,Item,Sample,Recorded Amount,Audited Amount\n"
                    "1,1,S1,1000,900\n"
                    "2,2,S2,2000,2000\n"
                    "3,3,S3,3000,3100\n"
                    "4,4,S4,4000,4000\n"
                ),
            }
        )

        population_count = 10
        sample_count = 4
        sum_difference = (1000 - 900) + (2000 - 2000) + (3000 - 3100) + (4000 - 4000)
        sum_difference_squared = (
            (1000 - 900) ** 2
            + (2000 - 2000) ** 2
            + (3000 - 3100) ** 2
            + (4000 - 4000) ** 2
        )
        average_difference = sum_difference / sample_count
        projection = average_difference * population_count
        std_dev = math.sqrt(
            (sum_difference_squared - sample_count * (average_difference**2))
            / sample_count
            - 1
        )
        cpi = population_count * 1.64 * (std_dev / math.sqrt(sample_count))
        upper = projection + cpi
        lower = projection - cpi

        self.assertAlmostEqual(worksheet.average_difference, average_difference, 2)
        self.assertAlmostEqual(
            worksheet.population_difference_projection, projection, 2
        )
        self.assertAlmostEqual(worksheet.population_standard_deviation, std_dev, 2)
        self.assertAlmostEqual(worksheet.computed_precision_interval, cpi, 2)
        self.assertAlmostEqual(worksheet.upper_confidence_limit, upper, 2)
        self.assertAlmostEqual(worksheet.lower_confidence_limit, lower, 2)

    def test_standard_deviation_zero_when_population_equals_sample(self):
        """Pure Python -- trigger P2 (L-04: no float tolerance in YAML
        ``equals``; asserts a zero result that depends on the same
        ``sqrt``-based compute chain as the previous test, so it is
        kept alongside it rather than split into YAML).

        Per ``ToD_akun_260821.ods`` cell ``D223``
        (``IF(population=sample,0,...)``): when the whole population
        was examined, the standard deviation is forced to 0 rather
        than computed from the sample.
        """
        worksheet, sd = self._create_worksheet_fixture(population_row_count=2)
        sd.write({"aria": "5"})
        worksheet.write(
            {
                "examination_data": (
                    "Seq,Item,Sample,Recorded Amount,Audited Amount\n"
                    "1,1,S1,1000,900\n"
                    "2,2,S2,2000,1900\n"
                ),
            }
        )

        self.assertEqual(worksheet.sample_count, 2)
        self.assertAlmostEqual(worksheet.population_standard_deviation, 0.0, 6)
        self.assertAlmostEqual(worksheet.computed_precision_interval, 0.0, 6)
