# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsB66777dTeamAllocation(HttpSavepointCase):
    """Tour test for the ``general_audit_ws_b66777d`` Final Team

    Allocations tab.
    """

    @classmethod
    def setUpClass(cls):
        """Create an Open worksheet with one contributing Team Member.

        The worksheet's own ``user_id`` (Responsible) is set to a
        dedicated user linked to a fresh ``hr.employee``, and its own
        ``preparation_time`` is filled -- so ``_populate_team_
        allocation()`` finds itself (every worksheet contributes to
        the search over ``general_audit_worksheet``) and the tour's
        Populate click has a real row to demonstrate.

        ``user_id`` is explicit throughout: ``cls.env`` runs as
        SUPERUSER, and the record rule
        ``general_audit_ws_b66777d_internal_user_rule`` would
        otherwise hide these fixtures from the tour's admin session
        (structure-and-runner.md "Fixture setUpClass berjalan sebagai
        SUPERUSER").
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        cls.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Audit Client - B66777D Team Allocation Tour",
                    "is_company": True,
                }
            )
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - B66777D Team Allocation Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-B66777D-TEAMALLOC-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Account Type Set - B66777D Team Allocation Tour",
                    "code": "/",
                }
            )
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Test Standard - B66777D Team Allocation Tour",
                    "code": "/",
                }
            )
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - B66777D Team Allocation Tour",
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

        team_user = (
            cls.env["res.users"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Team Allocation Tour User",
                    "login": "team_allocation_tour_user@example.com",
                    "email": "team_allocation_tour_user@example.com",
                }
            )
        )
        cls.env["hr.employee"].with_user(cls.admin).create(
            {
                "name": "Team Allocation Tour Employee",
                "user_id": team_user.id,
            }
        )

        ws_type_b66777d = cls.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_b66777d"
        )
        cls.worksheet = (
            cls.env["general_audit_ws_b66777d"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_b66777d.id,
                    "user_id": team_user.id,
                    "preparation_time": 8,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()

        cls.worksheet.invalidate_cache()

    def test_view_final_team_allocation(self):
        """Run the b66777d View Final Team Allocations tour.

        IK: docs/general_audit_ws_b66777d/02-view-final-team-allocation.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_final_report_b66777d_view_final_team_allocation",
            login="admin",
        )
