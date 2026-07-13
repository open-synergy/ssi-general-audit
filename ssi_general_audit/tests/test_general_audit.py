# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_test_helper import FakeModelLoader
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestGeneralAudit(YamlTransactionCase):
    def setUp(self):
        super().setUp()
        # `general_audit_worksheet_mixin` is a models.AbstractModel with no
        # concrete implementation inside this module (concrete worksheets
        # live in sibling modules this module cannot depend on). Register a
        # test-only concrete model so its compute/onchange logic can be
        # exercised here.
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import GeneralAuditWorksheetTester

        self.loader.update_registry((GeneralAuditWorksheetTester,))

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def test_general_audit(self):
        self.run_yaml_scenario("test_data_general_audit.yaml")

    def _create_minimal_general_audit(self):
        """Create a draft `general_audit` with only its required fields set."""
        partner = self.env["res.partner"].create(
            {"name": "Test Onchange Client", "is_company": True}
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Onchange Accountant"}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-ONCHANGE-0001",
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test Onchange Account Type Set", "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {"name": "Test Onchange Standard", "code": "/"}
        )
        return self.env["general_audit"].create(
            {
                "partner_id": partner.id,
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

    def test_onchange_type_id_sets_parent_type_id(self):
        """`onchange_parent_type_id` must copy `type_id` into `parent_type_id`."""
        audit = self._create_minimal_general_audit()
        worksheet_type = self.env["general_audit_worksheet_type"].create(
            {
                "name": "Test Onchange Worksheet Type",
                "code": "/",
                "model_name": "general_audit_worksheet_tester",
            }
        )

        form = Form(self.env["general_audit_worksheet_tester"])
        form.general_audit_id = audit
        form.type_id = worksheet_type

        self.assertEqual(form.parent_type_id, worksheet_type)
