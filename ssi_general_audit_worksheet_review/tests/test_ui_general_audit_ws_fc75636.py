# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsFc75636(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_fc75636`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open worksheet, then its Audit Final Memorandum sibling.

        The Pre-Condition (an On Progress Proposed Audit Opinion worksheet
        whose Audit Final Memorandum sibling only appears/opens AFTER the
        worksheet itself was created) is prepared here in Python, so the
        Links tab starts empty and the tour's Reload click has something
        real to demonstrate -- the compute only re-runs when
        ``general_audit_id`` changes, not when a sibling worksheet is
        created or opened later.

        Also creates an Open ``general_audit_ws_b66777d`` worksheet
        (``cls.final_worksheet``) under the same General Audit, for the
        b66777d "Fill Final Audit Opinion" tour
        (``ssi_general_audit_worksheet_final_report/docs/
        general_audit_ws_b66777d/01-fill-final-opinion.md``). That IK's
        module cannot host this tour itself: it depends on THIS module,
        never the other way around, so a fc75636 Populate source (here,
        ``cls.worksheet``, given a known ``draft_opinion`` text) can only
        exist together with a b66777d worksheet in a test suite on this
        side of the dependency. See
        ``GeneralAuditWSb66777d._populate_final_opinion()``'s docstring.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule general_audit_ws_fc75636_internal_user_rule
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
            .create({"name": "Test Audit Client - FC75636 Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - FC75636 Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-FC75636-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - FC75636 Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - FC75636 Tour", "code": "/"})
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - FC75636 Tour",
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

        ws_type_fc75636 = cls.env.ref(
            "ssi_general_audit_worksheet_review.worksheet_type_fc75636"
        )
        ws_type_a8c54f3 = cls.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_a8c54f3"
        )

        # The fc75636 worksheet is created FIRST, before its a8c54f3
        # sibling exists, so its audit_final_memorandum_id compute
        # resolves to False at creation time -- see the tour's
        # Post-Condition comment.
        cls.worksheet = (
            cls.env["general_audit_ws_fc75636"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_fc75636.id,
                }
            )
        )
        cls.worksheet.with_user(cls.admin).action_open()

        opinion = (
            cls.env["accountant.opinion"]
            .with_user(cls.admin)
            .create({"name": "Unqualified Opinion - FC75636 Tour", "code": "/"})
        )

        # Sibling worksheet the Reload button is expected to find. Opened
        # (not left in draft) -- the compute filters by
        # state in ["open", "done"].
        ws_memorandum = (
            cls.env["general_audit_ws_a8c54f3"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_a8c54f3.id,
                    "proposed_audit_opinion_id": opinion.id,
                }
            )
        )
        ws_memorandum.with_user(cls.admin).action_open()

        # Populate button source for the b66777d tour below: give
        # cls.worksheet's Opinion a known text so the tour's
        # post-Populate assertion has an exact string to match.
        cls.worksheet.with_user(cls.admin).write(
            {"draft_opinion": "Populate tour source text - Opinion"}
        )

        ws_type_b66777d = cls.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_b66777d"
        )
        cls.final_worksheet = (
            cls.env["general_audit_ws_b66777d"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_b66777d.id,
                }
            )
        )
        cls.final_worksheet.with_user(cls.admin).action_open()

        cls.worksheet.invalidate_cache()
        cls.final_worksheet.invalidate_cache()

    def test_reload_links(self):
        """Run the Reload Links tour.

        IK: docs/general_audit_ws_fc75636/01-reload_links.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_review_fc75636_reload_links",
            login="admin",
        )

    def test_fill_draft_opinion(self):
        """Run the Fill Draft Audit Opinion tour.

        IK: docs/general_audit_ws_fc75636/02-fill-draft-opinion.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_review_fc75636_fill_draft_opinion",
            login="admin",
        )

    def test_fill_final_opinion(self):
        """Run the b66777d Fill Final Audit Opinion tour.

        Module ``ssi_general_audit_worksheet_final_report``. IK:
        docs/general_audit_ws_b66777d/01-fill-final-opinion.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_review_b66777d_fill_final_opinion",
            login="admin",
        )
