# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSe3f4a5b(YamlTransactionCase):
    def setUp(self):
        """Build the fixtures shared by every scenario in
        ``test_data_general_audit_ws_e3f4a5b.yaml``.

        ``YamlTransactionCase.run_yaml_scenario`` only executes the
        top-level ``scenarios:`` key and resets ``self.registry`` before
        *each* scenario (see ``odoo_yaml_test.case.YamlTransactionCase``)
        - there is no ``setup:`` concept in the installed library (0.1.0),
        so a top-level ``setup:`` block in the YAML is silently never run.
        The shared fixtures are therefore built here instead and exposed
        as ``self.fx_<alias>`` attributes, which YAML steps reach through
        the ``EVAL:`` prefix (its expression context includes ``self`` -
        see ``odoo_yaml_test.case._parse_dynamic_value``), e.g.
        ``"EVAL: self.fx_audit.id"``. Unlike ``self.registry``, plain
        attributes on ``self`` survive the per-scenario reset.
        """
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        self.fx_client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - E3F4A5B", "is_company": True})
        )
        self.fx_accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - E3F4A5B"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": self.fx_accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-E3F4A5B-0001",
            }
        )
        self.fx_account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - E3F4A5B", "code": "/"})
        )
        self.fx_standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create(
                {"name": "Test Financial Accounting Standard - E3F4A5B", "code": "/"}
            )
        )
        self.fx_audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - E3F4A5B",
                    "partner_id": self.fx_client.id,
                    "accountant_id": self.fx_accountant.id,
                    "account_type_set_id": self.fx_account_type_set.id,
                    "financial_accounting_standard_id": self.fx_standard.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        self.fx_audit.with_user(admin).action_open()
        self.assertEqual(self.fx_audit.state, "open")

        self.fx_ws_type = env.ref(
            "ssi_general_audit_worksheet_test_of_control.worksheet_type_e3f4a5b"
        )
        self.fx_gl_ws_type = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        self.fx_sl_ws_type = env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_b5e3d9f"
        )

        self.fx_account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - E3F4A5B", "code": "/"})
        )
        self.fx_account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - E3F4A5B",
                    "code": "/",
                    "group_id": self.fx_account_group.id,
                    "normal_balance": "dr",
                    # DILARANG membiarkan python_code pada default
                    # "result = document.balance":
                    # general_audit.standard_detail._compute_extrapolation_balance
                    # akan crash (AttributeError) begitu tipe akun ini terhubung
                    # ke sebuah standard_detail.
                    "python_code": "result = 0.0",
                }
            )
        )
        self.fx_account = (
            env["client_account"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Client Account - E3F4A5B",
                    "code": "/",
                    "partner_id": self.fx_client.id,
                    "type_id": self.fx_account_type.id,
                }
            )
        )
        self.fx_conclusion = (
            env["general_audit_worksheet_conclusion"]
            .with_user(admin)
            .create(
                {
                    "name": "Control is operating effectively",
                    "code": "/",
                    "type_id": self.fx_ws_type.id,
                }
            )
        )

        raw_data_rows = "\n".join(
            f"REF-{i:04d},Note-{i:04d},Desc {i},{i * 100}.00" for i in range(1, 21)
        )
        self.fx_gl = (
            env["general_audit_ws_d209914"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.fx_audit.id,
                    "type_id": self.fx_gl_ws_type.id,
                    "account_mode": "account",
                    "account_id": self.fx_account.id,
                    "title": "Test GL Population",
                    "raw_data": "Ref,Note,Description,Amount\n" + raw_data_rows,
                }
            )
        )
        self.fx_subledger = (
            env["general_audit_ws_b5e3d9f"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.fx_audit.id,
                    "type_id": self.fx_sl_ws_type.id,
                    "account_mode": "account",
                    "account_id": self.fx_account.id,
                }
            )
        )

    def test_general_audit_ws_e3f4a5b(self):
        self.run_yaml_scenario("test_data_general_audit_ws_e3f4a5b.yaml")

    def _create_worksheet_fixture(self):
        """Build the minimal general_audit + worksheet fixture needed by the
        Python-only test below, entirely through the ORM (no demo data).
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - E3F4A5B Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - E3F4A5B Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-E3F4A5B-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - E3F4A5B Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - E3F4A5B Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - E3F4A5B Python",
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

        account_group = (
            env["client_account_group"]
            .with_user(admin)
            .create({"name": "Test Account Group - E3F4A5B Python", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - E3F4A5B Python",
                    "code": "/",
                    "group_id": account_group.id,
                    # No general_audit.standard_detail is created against this
                    # account type in this fixture, so the crashing default
                    # ("result = document.balance") is never evaluated here.
                    # Set explicitly anyway per the repo-wide convention of
                    # never leaving client_account_type.python_code at its
                    # default when general_audit.standard_detail could ever
                    # end up depending on it.
                    "python_code": "result = 0.0",
                }
            )
        )

        ws_type = env.ref(
            "ssi_general_audit_worksheet_test_of_control.worksheet_type_e3f4a5b"
        )
        worksheet = (
            env["general_audit_ws_e3f4a5b"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": ws_type.id})
        )
        return admin, worksheet, account_type

    def test_onchange_general_audit_id_clears_account_type(self):
        """``onchange_account_type_id`` is declared
        ``@api.onchange("general_audit_id")``, but ``account_type_id`` is only
        editable (``readonly=False``) while ``state == "open"``, and
        ``general_audit_id`` is only editable while ``state == "draft"`` -- the
        two conditions never overlap on the same record. Driving this through
        ``Form`` (the documented way to test onchange, see ``action: form`` in
        the odoo-yaml-test YAML DSL) is therefore impossible: setting
        ``account_type_id`` on a draft-state Form raises because the field is
        readonly at that state, and even if it could be set, ``Form.save()``
        explicitly does not persist readonly fields, so the onchange's
        in-memory clearing would be silently discarded on save whenever
        ``general_audit_id`` is actually editable. This exact limitation was
        already found and documented for the sibling ``general_audit_ws_b4f7d9c``
        worksheet in ``ssi_general_audit_worksheet_audit_procedure_vouching``
        -- it is a pre-existing pattern of the shared worksheet mixin's
        ``states`` design, not specific to this module. The onchange method is
        called directly here instead, to verify its own body does what it
        claims.
        """
        _admin, worksheet, account_type = self._create_worksheet_fixture()

        worksheet.sudo().write({"account_type_id": account_type.id})
        self.assertTrue(worksheet.account_type_id)

        worksheet.onchange_account_type_id()

        self.assertFalse(worksheet.account_type_id)

    def test_action_generate_sample_raises_without_raw_data(self):
        """Covers scenario 13 ("action_generate_sample gagal tanpa raw_data")
        from the YAML file, moved here because the installed odoo_yaml_test
        (0.1.0) has no `expect_error:` step handler (only `asserts:` after a
        successful call - see `_action_call` in `odoo_yaml_test/case.py`), so
        an exception raised by the called method cannot be declared as
        expected from YAML; it simply fails the step.
        """
        admin = self.env.ref("base.user_admin")
        worksheet = (
            self.env["general_audit_ws_e3f4a5b"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": self.fx_audit.id,
                    "type_id": self.fx_ws_type.id,
                }
            )
        )
        self.env["general_audit_ws_e3f4a5b.attribute"].with_user(admin).create(
            {
                "worksheet_id": worksheet.id,
                "name": "Otorisasi",
                "eper": 0.0,
                "tdr": 5,
                "aro": "5",
            }
        )

        with self.assertRaises(UserError) as cm:
            worksheet.with_user(admin).action_generate_sample()
        self.assertIn("No raw data available", str(cm.exception))
