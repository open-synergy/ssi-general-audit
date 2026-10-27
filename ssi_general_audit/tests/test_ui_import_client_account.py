# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiImportClientAccount(HttpSavepointCase):
    """Tour tests for the ``import_client_account`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit and an Open CoA and Mapping.

        The Pre-Condition of the import tour is prepared here in Python:
        an On Progress General Audit for a client named ``Test Audit
        Client - Import Account Tour`` and its CoA and Mapping document
        in Open status, the only status that shows Import Accounts.
        """
        super().setUpClass()
        # user_id is explicit: cls.env runs as SUPERUSER, and the record
        # rule of client_account_mapping would otherwise hide the fixture
        # from the tour's admin session.
        cls.admin = cls.env.ref("base.user_admin")
        env = cls.env

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = (
            env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Audit Client - Import Account Tour",
                    "is_company": True,
                }
            )
        )
        accountant = (
            env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - Import Account Tour"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-ICA-TOUR-0001",
            }
        )
        type_set = (
            env["client_account_type_set"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type Set - Import Account Tour",
                    "code": "/",
                }
            )
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - Import Account Tour", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - Import Account Tour",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": type_set.id,
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
        cls.mapping = (
            env["client_account_mapping"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id, "user_id": cls.admin.id})
        )
        # The state is reached through the action method, not write():
        # numbering is a side effect of it.
        cls.mapping.with_user(cls.admin).action_open()
        cls.mapping.invalidate_cache()

    def test_import(self):
        """Run the import tour for ``import_client_account``.

        IK: docs/import_client_account/01-import.md

        The tour stops at the Import dialog and closes it with Cancel: a
        file upload has no DOM completion signal. The preview and the
        imported accounts are covered by ``test_import_client_account``.
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_import_client_account_import",
            login="admin",
        )
