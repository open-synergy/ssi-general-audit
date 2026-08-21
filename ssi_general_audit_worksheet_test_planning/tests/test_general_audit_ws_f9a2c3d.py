# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAuditWSf9a2c3d(YamlTransactionCase):
    def test_general_audit_ws_f9a2c3d(self):
        self.run_yaml_scenario("test_data_general_audit_ws_f9a2c3d.yaml")

    def _create_worksheet_fixture(self, home_balance=8000.0):
        """Build the minimal general_audit + standard_detail (with a real,
        non-zero ``audited_balance`` rolled up from an actual home trial
        balance line) + worksheet fixture needed by the Python-only onchange
        tests below, entirely through the ORM (no demo data).

        ``general_audit.standard_detail.audited_balance`` is a stored
        compute (``_compute_adjustment_audited_balance``) that ultimately
        depends on ``home_standard_line_id`` -- itself a stored compute
        (``_compute_standard_line``) populated by a plain ``search()`` over
        ``client_trial_balance.standard_detail``, not by a declared
        ``@api.depends`` on that child model's creation. A real
        ``client_trial_balance`` + ``client_trial_balance.detail`` +
        ``client_trial_balance.standard_detail`` rollup is therefore built
        here, followed by an explicit ``invalidate_cache()`` so the whole
        chain (``home_standard_line_id`` -> ``home_statement_balance`` ->
        ``audited_balance``) reflects it -- same pattern documented in
        ``ssi_general_audit/tests/README_FIXTURE.md``.
        """
        env = self.env
        admin = env.ref("base.user_admin")

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Client - F9A2C3D Python", "is_company": True})
        )
        accountant = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - F9A2C3D Python"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-F9A2C3D-PYTHON-0001",
            }
        )
        account_type_set = (
            env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - F9A2C3D Python", "code": "/"})
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - F9A2C3D Python", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - F9A2C3D Python",
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
            .create({"name": "Test Account Group - F9A2C3D Python", "code": "/"})
        )
        account_type = (
            env["client_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type - F9A2C3D Python",
                    "code": "/",
                    "group_id": account_group.id,
                    "normal_balance": "dr",
                    # general_audit.standard_detail has no "balance" field,
                    # unlike client_trial_balance.standard_detail which the
                    # field's own default python_code
                    # ("result = document.balance") is written for. Use a
                    # safe no-op to avoid an unrelated crash in
                    # general_audit.standard_detail._compute_extrapolation_balance.
                    "python_code": "result = 0.0",
                }
            )
        )
        account_main = (
            env["client_account"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Client Account Main - F9A2C3D Python",
                    "code": "ACC-MAIN-F9A2C3D-PYTHON",
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
        )
        standard_detail = (
            env["general_audit.standard_detail"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "type_id": account_type.id})
        )
        tb_home = (
            env["client_trial_balance"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "trial_balance_type": "home"})
        )
        env["client_trial_balance.detail"].with_user(admin).create(
            {
                "trial_balance_id": tb_home.id,
                "account_id": account_main.id,
                "debit": home_balance,
            }
        )
        env["client_trial_balance.standard_detail"].with_user(admin).create(
            {
                "trial_balance_id": tb_home.id,
                "standard_detail_id": standard_detail.id,
            }
        )
        standard_detail.invalidate_cache()
        self.assertEqual(standard_detail.audited_balance, home_balance)

        ws_type = env.ref(
            "ssi_general_audit_worksheet_test_planning.worksheet_type_f9a2c3d"
        )
        worksheet = (
            env["general_audit_ws_f9a2c3d"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type.id,
                    "standard_detail_id": standard_detail.id,
                }
            )
        )
        return admin, audit, account_type, client, worksheet

    def _create_audit_detail(
        self, admin, audit, account_type, client, code_suffix, balance
    ):
        """Create a ``general_audit.detail`` line with a real, non-zero
        ``audited_balance`` (sourced from a genuine home trial balance
        line), for use by the detail-model onchange tests below.
        """
        env = self.env
        account = (
            env["client_account"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Client Account %s - F9A2C3D Python" % code_suffix,
                    "code": "ACC-%s-F9A2C3D-PYTHON" % code_suffix,
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
        )
        tb_home = env["client_trial_balance"].search(
            [("general_audit_id", "=", audit.id), ("trial_balance_type", "=", "home")],
            limit=1,
        )
        env["client_trial_balance.detail"].with_user(admin).create(
            {
                "trial_balance_id": tb_home.id,
                "account_id": account.id,
                "debit": balance,
            }
        )
        audit_detail = (
            env["general_audit.detail"]
            .with_user(admin)
            .create({"general_audit_id": audit.id, "account_id": account.id})
        )
        audit_detail.invalidate_cache()
        self.assertEqual(audit_detail.audited_balance, balance)
        return audit_detail

    def test_onchange_direct_examination_sets_key_item_amount(self):
        """``_onchange_examination_sampling`` on the header model
        (``general_audit_ws_f9a2c3d``) is declared
        ``@api.onchange("standard_detail_id", "direct_examination",
        "need_sampling")``. Its view (``views/general_audit_ws_f9a2c3d.xml``)
        renders ``allowed_standard_detail_ids`` and
        ``allowed_preliminary_materiality_ids`` as ``invisible="1"``
        Many2many fields with **no** tree sub-arch -- exactly the
        pre-existing pattern already found (and documented) for the sibling
        worksheet ``general_audit_ws_f9a2c3d``'s cousins in BL-0171
        (``ssi_general_audit_worksheet_sample_determination``/
        ``ssi_general_audit_worksheet_test_of_control``): ``Form()``/
        ``action: form`` fails for any model whose view contains an
        invisible Many2many with no sub-view arch, raising
        ``AssertionError: __len__ was not found in the view``. Rather than
        spend a whole CI cycle proving that failure for this module too, the
        onchange method is called directly on a real ORM record here -- it
        is production code already shipped by this module, so no
        ``odoo_test_helper``/``FakeModelLoader`` trick is needed.
        """
        (
            _admin,
            _audit,
            _account_type,
            _client,
            worksheet,
        ) = self._create_worksheet_fixture(home_balance=8000.0)

        worksheet.sudo().write({"direct_examination": True, "need_sampling": False})
        self.assertEqual(worksheet.key_item_amount, 0.0)

        worksheet._onchange_examination_sampling()

        self.assertEqual(worksheet.key_item_amount, worksheet.audited_balance)
        self.assertEqual(worksheet.key_item_amount, 8000.0)

    def test_onchange_need_sampling_clears_key_item_amount(self):
        """See ``test_onchange_direct_examination_sets_key_item_amount`` for
        why this onchange is verified by calling the method directly instead
        of through ``Form``.
        """
        (
            _admin,
            _audit,
            _account_type,
            _client,
            worksheet,
        ) = self._create_worksheet_fixture(home_balance=8000.0)
        worksheet.sudo().write({"key_item_amount": 8000.0})

        worksheet.sudo().write({"direct_examination": False, "need_sampling": True})
        worksheet._onchange_examination_sampling()

        self.assertEqual(worksheet.key_item_amount, 0.0)

    def test_onchange_detail_direct_examination_sets_key_item_amount(self):
        """Same onchange, declared on the detail model
        (``general_audit_ws_f9a2c3d.detail``,
        ``@api.onchange("audit_detail_id", "direct_examination",
        "need_sampling")``). The detail model's own tree view
        (``general_audit_ws_f9a2c3d_detail_view_tree``, also embedded in the
        header form) renders ``allowed_audit_detail_ids`` as
        ``invisible="1"`` with no sub-arch either, so the same ``Form()``
        limitation applies -- see the header test's docstring above.
        """
        admin, audit, account_type, client, worksheet = self._create_worksheet_fixture(
            home_balance=8000.0
        )
        audit_detail = self._create_audit_detail(
            admin, audit, account_type, client, "DIRECT-EXAM", 4500.0
        )
        detail_line = (
            self.env["general_audit_ws_f9a2c3d.detail"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": worksheet.id,
                    "audit_detail_id": audit_detail.id,
                    "direct_examination": True,
                    "need_sampling": False,
                }
            )
        )
        self.assertEqual(detail_line.key_item_amount, 0.0)

        detail_line._onchange_examination_sampling()

        self.assertEqual(detail_line.key_item_amount, detail_line.audited_balance)
        self.assertEqual(detail_line.key_item_amount, 4500.0)

    def test_onchange_detail_need_sampling_clears_key_item_amount(self):
        """See
        ``test_onchange_detail_direct_examination_sets_key_item_amount`` for
        why this onchange is verified by calling the method directly instead
        of through ``Form``.
        """
        admin, audit, account_type, client, worksheet = self._create_worksheet_fixture(
            home_balance=8000.0
        )
        audit_detail = self._create_audit_detail(
            admin, audit, account_type, client, "NEED-SAMPLING", 4500.0
        )
        detail_line = (
            self.env["general_audit_ws_f9a2c3d.detail"]
            .with_user(admin)
            .create(
                {
                    "worksheet_id": worksheet.id,
                    "audit_detail_id": audit_detail.id,
                    "key_item_amount": 4500.0,
                }
            )
        )

        detail_line.sudo().write({"direct_examination": False, "need_sampling": True})
        detail_line._onchange_examination_sampling()

        self.assertEqual(detail_line.key_item_amount, 0.0)
