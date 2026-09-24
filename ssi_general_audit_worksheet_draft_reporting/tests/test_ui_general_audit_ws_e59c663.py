# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixtures below need it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsE59c663(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_e59c663`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create three open General Audits plus a draft and an open worksheet.

        ``cls.worksheet_draft`` (state ``draft``) is the Pre-Condition for
        the Open/Start tour, and ``cls.worksheet_open`` (state ``open``) is
        the Pre-Condition for the Confirm tour. ``cls.audit`` itself is
        reserved for the Create tour, which selects it by title through
        the UI and creates its own worksheet against it -- it must stay
        free of a pre-existing e59c663 worksheet for that to succeed.

        Three separate ``general_audit`` records are needed (one per
        worksheet-bearing fixture, plus ``cls.audit``) because
        ``general_audit_worksheet_mixin``'s ``_check_unique_general_audit``
        constraint allows at most one ``general_audit_ws_e59c663`` per
        ``general_audit`` -- creating two such worksheets against the same
        audit, or having the Create tour target an audit that already has
        one, raises a ValidationError on the offending ``create()``.

        ``cls.worksheet_open`` also has its ``conclusion_id``/``conclusion``
        pre-filled here (below), so the Confirm tour only has to click the
        Confirm button rather than select a value from the ``conclusion_id``
        many2one dropdown itself.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and the
        # record rule general_audit_ws_e59c663_internal_user_rule would
        # otherwise hide these fixtures from the tour's admin session (see
        # structure-and-runner.md "Fixture setUpClass berjalan sebagai
        # SUPERUSER").
        cls.admin = cls.env.ref("base.user_admin")

        cls.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )

        client = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Client - E59C663 Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - E59C663 Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-E59C663-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - E59C663 Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - E59C663 Tour", "code": "/"})
        )
        cls.audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - E59C663 Tour",
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
        cls.audit.with_user(cls.admin).action_open()

        # Two more separate General Audits -- see the class docstring for
        # why ``worksheet_draft``/``worksheet_open`` cannot share an audit
        # with each other or with ``cls.audit`` (reserved for the Create
        # tour, and left without a pre-existing worksheet). Their titles
        # deliberately do NOT contain "Test General Audit - E59C663 Tour"
        # as a substring: the Create tour's autocomplete step matches
        # ``:contains(Test General Audit - E59C663 Tour)``, and with 3
        # overlapping titles Odoo's dropdown picked a "Create and Edit"
        # quick-create entry instead of the intended existing record
        # (confirmed from the CI failure screenshot -- a blank "Create:
        # General Audit" dialog popped up instead of the field being
        # filled from an existing one).
        audit_for_draft = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "E59C663 Tour Fixture - Draft Worksheet",
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
        audit_for_draft.with_user(cls.admin).action_open()

        audit_for_open = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "E59C663 Tour Fixture - Open Worksheet",
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
        audit_for_open.with_user(cls.admin).action_open()

        ws_type = cls.env.ref(
            "ssi_general_audit_worksheet_draft_reporting.worksheet_type_e59c663"
        )

        # Selectable from the Confirm tour's Conclusion field.
        cls.conclusion = (
            cls.env["general_audit_worksheet_conclusion"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Complete - E59C663 Tour",
                    "code": "/",
                    "type_id": ws_type.id,
                }
            )
        )

        # Pre-Condition for the Open/Start tour: stays in draft.
        cls.worksheet_draft = (
            cls.env["general_audit_ws_e59c663"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit_for_draft.id, "type_id": ws_type.id})
        )

        # Pre-Condition for the Confirm tour: already started.
        cls.worksheet_open = (
            cls.env["general_audit_ws_e59c663"]
            .with_user(cls.admin)
            .create({"general_audit_id": audit_for_open.id, "type_id": ws_type.id})
        )
        cls.worksheet_open.with_user(cls.admin).action_open()

        # Pre-filled here rather than through the Confirm tour: selecting
        # ``conclusion_id`` from its dropdown was found to leave the
        # many2one widget without an <input> in the CI browser -- see the
        # PR discussion for ssi-general-audit#391/#392. The Confirm tour's
        # actual scope is the Confirm button and workflow transition;
        # asserting a specific selected/saved value is unit-test territory
        # (odoo-development-ui-test skill scope: "Tour TIDAK menguji
        # nilai"), so the value is set directly here instead.
        cls.worksheet_open.with_user(cls.admin).write(
            {
                "conclusion_id": cls.conclusion.id,
                "conclusion": "Draft financial statements reviewed against WR.160.1.",
            }
        )

        cls.worksheet_draft.invalidate_cache()
        cls.worksheet_open.invalidate_cache()

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_e59c663/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_e59c663_create",
            login="admin",
        )

    def test_open(self):
        """Run the Open (Start) tour.

        IK: docs/general_audit_ws_e59c663/08-open.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_e59c663_open",
            login="admin",
        )

    def test_confirm(self):
        """Run the Confirm tour.

        IK: docs/general_audit_ws_e59c663/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_draft_reporting_e59c663_confirm",
            login="admin",
        )
