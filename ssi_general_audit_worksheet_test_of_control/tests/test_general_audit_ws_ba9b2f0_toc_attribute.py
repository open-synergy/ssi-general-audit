# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import tagged
from odoo.tests.common import Form, TransactionCase


@tagged("post_install", "-at_install")
class TestGeneralAuditWSba9b2f0TocAttribute(TransactionCase):
    """Covers `general_audit_ws_ba9b2f0.detail.toc_attribute_id` and the
    `toc_analysis`/`toc_reference` related fields added on top of it in
    `models/ba9b2f0/general_audit_ws_ba9b2f0_detail.py` (this module).

    Mirrors ``test_general_audit_ws_eabdaad_toc_attribute.py`` (HT/26/000631)
    - HT/26/000658 asked for the same ToC-attribute link on the "Significant
    Account" (ba9b2f0) worksheet. The only structural difference is the
    scoping key: eabdaad scopes by ``business_cycle_id``/``cycle_id``, while
    ba9b2f0/e3f4a5b both scope by ``account_type_id`` - no business cycle
    involved here.
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
            .create({"name": "Test Audit Client - BA9B2F0 ToC", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - BA9B2F0 ToC"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-BA9B2F0-TOC-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - BA9B2F0 ToC", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - BA9B2F0 ToC", "code": "/"})
        )
        self.audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - BA9B2F0 ToC",
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
        key_internal_control = env.ref(
            "ssi_general_audit_worksheet_control_risk"
            ".general_audit_account_key_internal_control_kic001"
        )

        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - BA9B2F0 ToC", "code": "/"})
        )
        # See the same DILARANG note in test_general_audit_ws_e3f4a5b.py: never
        # leave python_code at its crashing default.
        self.account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - BA9B2F0 ToC",
                    "code": "/",
                    "group_id": account_group.id,
                    "python_code": "result = 0.0",
                }
            )
        )
        self.other_account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - BA9B2F0 ToC (Other)",
                    "code": "/",
                    "group_id": account_group.id,
                    "python_code": "result = 0.0",
                }
            )
        )

        ba9b2f0_ws_type = env.ref(
            "ssi_general_audit_worksheet_control_risk.worksheet_type_ba9b2f0"
        )
        ba9b2f0_worksheet = (
            env["general_audit_ws_ba9b2f0"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.audit.id,
                    "type_id": ba9b2f0_ws_type.id,
                    "account_type_id": self.account_type.id,
                }
            )
        )
        self.detail = (
            env["general_audit_ws_ba9b2f0.detail"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": ba9b2f0_worksheet.id,
                    "key_internal_control_id": key_internal_control.id,
                    "name": "Test control activity",
                    "frequency": "Monthly",
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
                    "account_type_id": self.account_type.id,
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
                    "account_type_id": self.other_account_type.id,
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

        # A second attribute belonging to a DIFFERENT engagement/account type,
        # used to verify the toc_attribute_id domain (mirrored in
        # views/general_audit_ws_ba9b2f0_views.xml) actually excludes it.
        self.other_account_type_attribute = (
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
        # toc_reference is Many2one (HT/26/000658: made clickable in the UI
        # instead of a plain text document number, mirroring HT/26/000631's
        # fix on the "Control Risk - Cycle Level" (eabdaad) worksheet).
        self.assertEqual(self.detail.toc_reference, self.toc_attribute.worksheet_id)
        # rely_on_control == "yes" (see setUp) + toc_analysis == "effective"
        # (via the link above) -> _compute_result's "low" branch.
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

    def test_toc_attribute_domain_excludes_other_engagement_and_account_type(self):
        # Same domain as `toc_attribute_id` in
        # views/general_audit_ws_ba9b2f0_views.xml.
        domain = [
            (
                "worksheet_id.general_audit_id",
                "=",
                self.detail.worksheet_id.general_audit_id.id,
            ),
            (
                "worksheet_id.account_type_id",
                "=",
                self.detail.worksheet_id.account_type_id.id,
            ),
        ]
        candidates = self.env["general_audit_ws_e3f4a5b.attribute"].search(domain)

        self.assertIn(self.toc_attribute, candidates)
        self.assertNotIn(self.other_account_type_attribute, candidates)

    def test_onchange_rely_on_control_no_clears_toc_link(self):
        """HT/26/000658: ToC Attribute/Reference/Analysis must not stay
        filled once "Rely on Control" is switched to "No" - clearing
        toc_attribute_id also cascades to toc_analysis/toc_reference since
        both are related to it.

        No dedicated form view is registered for
        ``general_audit_ws_ba9b2f0.detail`` (only an inline ``<form>``
        embedded in the parent's one2many), so ``Form()`` cannot target it
        directly - the onchange method is invoked directly instead, same as
        Odoo's onchange dispatch would do after ``rely_on_control`` changes.
        """
        self.detail.write({"toc_attribute_id": self.toc_attribute.id})
        self.assertEqual(self.detail.toc_analysis, "effective")
        self.assertEqual(self.detail.toc_reference, self.toc_attribute.worksheet_id)

        self.detail.rely_on_control = "no"
        self.detail.onchange_rely_on_control()

        self.assertFalse(self.detail.toc_attribute_id)
        self.assertFalse(self.detail.toc_analysis)
        self.assertFalse(self.detail.toc_reference)

    def test_onchange_rely_on_control_yes_keeps_toc_link(self):
        """Switching (or staying) on "Yes" must not clear an already-picked
        ToC Attribute."""
        self.detail.write({"toc_attribute_id": self.toc_attribute.id})

        self.detail.rely_on_control = "yes"
        self.detail.onchange_rely_on_control()

        self.assertEqual(self.detail.toc_attribute_id, self.toc_attribute)

    def test_switching_to_no_and_saving_actually_clears_toc_link(self):
        """HT/26/000658 follow-up: the onchange-computed clear must survive
        a real save through the UI's form/one2many machinery, not just an
        in-memory/direct-write check.

        ``toc_attribute_id`` is ``attrs``-readonly whenever
        ``rely_on_control != "yes"``. Odoo's web client (and ``Form()``,
        which mirrors it) drops fields that are readonly in the record's
        *final* state from the write payload entirely - so without the
        ``write()`` override, switching to "No" and saving would silently
        keep the OLD ``toc_attribute_id``/``toc_analysis``/``toc_reference``
        in the database even though the form showed them blank right before
        saving.
        """
        worksheet = self.detail.worksheet_id
        worksheet.with_user(self.admin).action_open()

        with Form(worksheet.with_user(self.admin)) as worksheet_form:
            with worksheet_form.detail_ids.edit(0) as line:
                line.toc_attribute_id = self.toc_attribute

        self.detail.invalidate_cache()
        self.assertEqual(self.detail.toc_attribute_id, self.toc_attribute)
        self.assertEqual(self.detail.toc_analysis, "effective")

        with Form(worksheet.with_user(self.admin)) as worksheet_form:
            with worksheet_form.detail_ids.edit(0) as line:
                line.rely_on_control = "no"

        self.detail.invalidate_cache()
        self.assertFalse(
            self.detail.toc_attribute_id,
            "toc_attribute_id must stay cleared after save, not silently "
            "revert to the value it had before switching to 'No'.",
        )
        self.assertFalse(self.detail.toc_analysis)
        self.assertFalse(self.detail.toc_reference)
