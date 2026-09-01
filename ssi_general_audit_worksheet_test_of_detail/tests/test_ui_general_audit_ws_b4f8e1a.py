# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsB4f8e1a(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_b4f8e1a`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the engagement, General Ledger, and open worksheet.

        Everything the tour itself is meant to exercise (Data Mode,
        General Ledger, Data Source, and the Generate Examination Data
        click) is left blank/default here -- the tour fills those in
        through the UI. Identifier Column Number is configured on the
        General Ledger itself, not on this worksheet (that field was
        removed from ``general_audit_ws_b4f8e1a`` -- see
        ``general_audit_ws_d209914``/``general_audit_ws_b5e3d9f``), so
        it is set here as part of the Pre-Condition rather than
        through the tour. The Pre-Condition (an On Progress worksheet
        linked to an engagement with a General Ledger already
        imported, its Identifier Column Number already configured) is
        prepared in Python.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule general_audit_ws_b4f8e1a_internal_user_rule
        # would otherwise hide these fixtures from the tour's admin
        # session (structure-and-runner.md "Fixture setUpClass berjalan
        # sebagai SUPERUSER").
        cls.admin = cls.env.ref("base.user_admin")

        cls.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Client - B4F8E1A Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - B4F8E1A Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-B4F8E1A-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - B4F8E1A Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - B4F8E1A Tour", "code": "/"})
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - B4F8E1A Tour",
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
        audit.with_user(cls.admin).action_open()

        ws_type_d209914 = cls.env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        # Sole data row, one identifier value: the tour selects this GL
        # by being the only option in its dropdown (no name-based
        # search), then asserts on this exact identifier after Generate
        # Examination Data -- it cannot appear on the form any other way.
        cls.gl = (
            cls.env["general_audit_ws_d209914"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_d209914.id,
                    "raw_data": "Ref,Debit,Credit\nTOUR-B4F8E1A-R1,1000,0\n",
                    "debit_col_number": 2,
                    "credit_col_number": 3,
                    "identifier_col_number": 1,
                }
            )
        )

        ws_type = cls.env.ref(
            "ssi_general_audit_worksheet_test_of_detail.worksheet_type_b4f8e1a"
        )
        cls.worksheet = (
            cls.env["general_audit_ws_b4f8e1a"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type.id,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()
        cls.worksheet.invalidate_cache()

    def test_generate_examination_data(self):
        """Run the fill-Data-and-Generate tour for ``general_audit_ws_b4f8e1a``.

        IK: docs/general_audit_ws_b4f8e1a/01-isi-data-dan-generate.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_test_of_detail_b4f8e1a_generate_examination_data",
            login="admin",
        )
