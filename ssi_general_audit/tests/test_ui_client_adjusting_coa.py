# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiClientAdjustingCoa(HttpSavepointCase):
    """Tour tests for the ``client_adjusting_coa`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit and two Adjusting CoA documents.

        The Pre-Condition of every tour is prepared here in Python: an
        On Progress General Audit named ``TOUR-ACOA-GA`` whose account
        type set holds the type ``TOUR-ACOA-TYPE``, one document in Draft
        (confirm tour) and one waiting for approval (approve tour). The
        create tour builds its own document through the UI.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule client_adjusting_coa_internal_user_rule would
        # otherwise hide these fixtures from the tour's admin session
        # (structure-and-runner.md "Fixture setUpClass berjalan sebagai
        # SUPERUSER").
        cls.admin = cls.env.ref("base.user_admin")
        env = cls.env

        env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = (
            env["res.partner"]
            .with_user(cls.admin)
            .create(
                {"name": "Test Audit Client - Adjusting CoA Tour", "is_company": True}
            )
        )
        accountant = (
            env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - Adjusting CoA Tour"})
        )
        cpa_category = env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-ACOA-TOUR-0001",
            }
        )
        group = (
            env["client_account_group"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR-ACOA-GROUP",
                    "code": "/",
                    "sequence": 1,
                    "normal_balance": "dr",
                }
            )
        )
        account_type = (
            env["client_account_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR-ACOA-TYPE",
                    "code": "/",
                    "group_id": group.id,
                    "sequence": 1,
                    "normal_balance": "dr",
                    # DILARANG membiarkan python_code pada default
                    # "result = document.balance": crash pada extrapolation
                    # balance.
                    "python_code": "result = 0.0",
                }
            )
        )
        type_set = (
            env["client_account_type_set"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type Set - Adjusting CoA Tour",
                    "code": "/",
                    "detail_ids": [(6, 0, [account_type.id])],
                }
            )
        )
        standard = (
            env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - Adjusting CoA Tour", "code": "/"})
        )
        audit = (
            env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - Adjusting CoA Tour",
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
        # The tour picks the General Audit by this fixed number, because
        # the generated one changes on every run.
        audit.sudo().write({"name": "TOUR-ACOA-GA"})

        old_account = (
            env["client_account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Client Account - Adjusting CoA Tour",
                    "code": "ACC-ACOA-TOUR",
                    "partner_id": client.id,
                    "type_id": account_type.id,
                }
            )
        )
        mapping = (
            env["client_account_mapping"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit.id})
        )
        env["client_account_mapping.detail"].with_user(cls.admin).create(
            {
                "mapping_id": mapping.id,
                "account_id": old_account.id,
                "type_id": account_type.id,
            }
        )
        audit.with_user(cls.admin).action_reload_account()
        audit.with_user(cls.admin).action_reload_standard_account()

        cls.draft_doc = cls._create_document(audit, account_type, "TOUR-ACOA-D1")
        cls.waiting_doc = cls._create_document(audit, account_type, "TOUR-ACOA-C1")
        # The state is reached through the action method, not write():
        # numbering and approval records are side effects of it.
        cls.waiting_doc.with_user(cls.admin).action_confirm()
        cls.waiting_doc.invalidate_cache()

    @classmethod
    def _create_document(cls, audit, account_type, code):
        """Create an Adjusting CoA document with one line.

        :param audit: ``general_audit`` that receives the account
        :param account_type: ``client_account_type`` of the line
        :param code: code of the new account
        :return: the ``client_adjusting_coa`` record, in Draft
        """
        return (
            cls.env["client_adjusting_coa"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "user_id": cls.admin.id,
                    "detail_ids": [
                        (
                            0,
                            0,
                            {
                                "code": code,
                                "name": "Tour Account %s" % code,
                                "type_id": account_type.id,
                            },
                        )
                    ],
                }
            )
        )

    def test_create(self):
        """Run the create tour for ``client_adjusting_coa``.

        IK: docs/client_adjusting_coa/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_client_adjusting_coa_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``client_adjusting_coa``.

        IK: docs/client_adjusting_coa/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_client_adjusting_coa_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``client_adjusting_coa``.

        IK: docs/client_adjusting_coa/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_client_adjusting_coa_approve",
            login="admin",
        )
