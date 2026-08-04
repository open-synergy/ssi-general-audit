# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGeneralAuditWSeabdaadTocAttribute(TransactionCase):
    """Covers `general_audit_ws_eabdaad.detail.toc_attribute_id` and the
    `toc_analysis`/`toc_reference` related fields added on top of it in
    `models/eabdaad/general_audit_ws_eabdaad_detail.py` (this module).

    Plain ``TransactionCase`` rather than the YAML DSL used by
    ``test_general_audit_ws_e3f4a5b.py`` - this fixture chain is deep
    (general_audit -> two worksheets -> detail/attribute) and the assertions
    below (recompute propagation, engagement+cycle domain filtering) are
    easier to express directly against the ORM than through the YAML
    scenario primitives (create/write/call/assert/ref/search).
    """

    def setUp(self):
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        self.admin = admin

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - EABDAAD ToC", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - EABDAAD ToC"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-EABDAAD-TOC-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - EABDAAD ToC", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - EABDAAD ToC", "code": "/"})
        )
        self.audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - EABDAAD ToC",
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
        self.audit.with_user(admin).action_open()

        # Reusable master data shipped by the modules themselves (data/master/),
        # not test-specific - always present once the modules are installed.
        self.cycle = env.ref("ssi_general_audit.client_business_process_2_ef83aa88")
        self.other_cycle = env.ref(
            "ssi_general_audit.client_business_process_1_b172f8c6"
        )
        key_internal_control = env.ref(
            "ssi_general_audit_worksheet_control_risk"
            ".general_audit_key_internal_control_86_8b14c4f6"
        )

        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - EABDAAD ToC", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - EABDAAD ToC",
                    "code": "/",
                    "group_id": account_group.id,
                    # See the same DILARANG note in test_general_audit_ws_e3f4a5b.py:
                    # never leave python_code at its crashing default.
                    "python_code": "result = 0.0",
                }
            )
        )

        eabdaad_ws_type = env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_eabdaad"
        )
        eabdaad_worksheet = (
            env["general_audit_ws_eabdaad"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": eabdaad_ws_type.id,
                    "business_cycle_id": self.cycle.id,
                }
            )
        )
        self.detail = (
            env["general_audit_ws_eabdaad.detail"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": eabdaad_worksheet.id,
                    "key_internal_control_id": key_internal_control.id,
                    "name": "Test control activity",
                    "frequency": "Monthly",
                    "related_account_type_ids": [(6, 0, [account_type.id])],
                    "rely_on_control": "yes",
                }
            )
        )

        e3f4a5b_ws_type = env.ref(
            "ssi_general_audit_worksheet_test_of_control.worksheet_type_e3f4a5b"
        )
        self.toc_worksheet = (
            env["general_audit_ws_e3f4a5b"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": e3f4a5b_ws_type.id,
                    "cycle_id": self.cycle.id,
                }
            )
        )
        other_toc_worksheet = (
            env["general_audit_ws_e3f4a5b"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": e3f4a5b_ws_type.id,
                    "cycle_id": self.other_cycle.id,
                }
            )
        )

        # n=25, k=0 -> cuer_5pct=11.3, cuer_10pct=8.8 (same deterministic
        # fixture data already relied on in test_data_general_audit_ws_e3f4a5b.yaml).
        sample_data = "Seq,Deviation\n" + "\n".join(f"{i},FALSE" for i in range(1, 26))
        self.toc_attribute = (
            env["general_audit_ws_e3f4a5b.attribute"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": self.toc_worksheet.id,
                    "name": "Otorisasi",
                    "eper": 0.0,
                    "tdr": 5,
                    "aro": "10",
                    "sample_data": sample_data,
                }
            )
        )
        self.toc_attribute.action_compute_deviation()
        self.assertEqual(self.toc_attribute.conclusion, "effective")

        # A second attribute belonging to a DIFFERENT engagement/cycle, used to
        # verify the toc_attribute_id domain (mirrored in
        # views/general_audit_ws_eabdaad_views.xml) actually excludes it.
        self.other_cycle_attribute = (
            env["general_audit_ws_e3f4a5b.attribute"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": other_toc_worksheet.id,
                    "name": "Verifikasi",
                    "eper": 0.0,
                    "tdr": 5,
                    "aro": "5",
                }
            )
        )

    def test_toc_attribute_pulls_analysis_and_reference(self):
        self.assertFalse(self.detail.toc_analysis)
        self.assertFalse(self.detail.toc_reference)

        self.detail.write({"toc_attribute_id": self.toc_attribute.id})

        self.assertEqual(self.detail.toc_analysis, self.toc_attribute.conclusion)
        self.assertEqual(self.detail.toc_analysis, "effective")
        self.assertEqual(
            self.detail.toc_reference, self.toc_attribute.worksheet_id.name
        )
        # rely_on_control == "yes" (see setUp) + toc_analysis == "effective"
        # (via the link above) -> _compute_result's "low" branch. This is the
        # branch ssi_general_audit_worksheet_control_risk's own
        # test_data_ws_internal_control.yaml can no longer reach on its own
        # now that toc_analysis is related+readonly - covered here instead.
        self.assertEqual(self.detail.result, "low")

    def test_toc_analysis_recomputes_when_attribute_conclusion_changes(self):
        self.detail.write({"toc_attribute_id": self.toc_attribute.id})
        self.assertEqual(self.detail.toc_analysis, "effective")

        # aro 10 -> cuer_10pct=8.8 (<=10, effective); aro 5 -> cuer_5pct=11.3
        # (>5, not_effective). Same flip already exercised in
        # test_data_general_audit_ws_e3f4a5b.yaml scenario 7.
        self.toc_attribute.write({"aro": "5"})

        self.assertEqual(self.toc_attribute.conclusion, "not_effective")
        self.assertEqual(
            self.detail.toc_analysis,
            "not_effective",
            "toc_analysis must follow the linked attribute's conclusion "
            "automatically (related + store=True), with no action needed "
            "on the detail record itself.",
        )

    def test_toc_attribute_domain_excludes_other_engagement_and_cycle(self):
        # Same domain as `toc_attribute_id` in
        # views/general_audit_ws_eabdaad_views.xml.
        domain = [
            (
                "worksheet_id.general_audit_id",
                "=",
                self.detail.worksheet_id.general_audit_id.id,
            ),
            (
                "worksheet_id.cycle_id",
                "=",
                self.detail.worksheet_id.business_cycle_id.id,
            ),
        ]
        candidates = self.env["general_audit_ws_e3f4a5b.attribute"].search(domain)

        self.assertIn(self.toc_attribute, candidates)
        self.assertNotIn(self.other_cycle_attribute, candidates)
