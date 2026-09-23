# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWSFinalReport(YamlTransactionCase):
    """Scenario tests for the ``ssi_general_audit_worksheet_final_report``
    worksheets."""

    def test_ws_final_report(self):
        """Run the CRUD/populate/aggregation YAML scenarios."""
        self.run_yaml_scenario("test_data_ws_final_report.yaml")

    def _create_general_audit_for_source_worksheets(self, name_suffix):
        """Create and open a minimal ``general_audit`` for a fixture.

        Fixture built in Python (P10: shared setup for the Python-only
        test method below -- the YAML scenario registry used by
        ``run_yaml_scenario`` does not survive into a plain
        ``TransactionCase`` method, ``python-escape-hatch.md`` rule 6).

        :param str name_suffix: text appended to record names so
            fixtures from different test methods stay distinguishable
        :return: the ``general_audit`` record, already opened
        :rtype: recordset
        """
        config_parameter = self.env["ir.config_parameter"].sudo()
        config_parameter.set_param("ssi_general_audit.max_number_of_cpa_license", "100")

        client = self.env["res.partner"].create(
            {
                "name": "Test Audit Client - %s" % name_suffix,
                "is_company": True,
            }
        )
        accountant = self.env["res.partner"].create(
            {"name": "Test Audit Accountant - %s" % name_suffix}
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-%s-0001" % name_suffix,
            }
        )
        account_type_set = self.env["client_account_type_set"].create(
            {"name": "Test Account Type Set - %s" % name_suffix, "code": "/"}
        )
        standard = self.env["accountant.financial_accounting_standard"].create(
            {
                "name": "Test Financial Accounting Standard - %s" % name_suffix,
                "code": "/",
            }
        )
        audit = self.env["general_audit"].create(
            {
                "title": "Test General Audit - %s" % name_suffix,
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
        audit.action_open()
        return audit

    def test_action_view_source_worksheets_domain(self):
        """Assert the domain returned by ``action_view_source_worksheets``.

        Pure Python -- trigger P1 (L-01: ``action: call`` in YAML
        discards a method's return value, so the ``ir.actions.act_
        window`` dict this button returns can never be asserted from
        YAML at all). Builds one ``general_audit_ws_b66777d.team_
        allocation`` row for an employee who contributes to TWO
        worksheets of the same engagement -- one via preparation, one
        via review -- plus a THIRD worksheet of the SAME engagement
        contributed by a different employee (must be excluded) and a
        FOURTH worksheet of a DIFFERENT engagement contributed by the
        SAME employee (must also be excluded, since it belongs to
        another ``general_audit``). Feeding the action's returned
        domain into a fresh ``search()`` on ``general_audit_worksheet``
        must come back with EXACTLY the first two worksheets.

        :return: nothing; asserts the action dict's shape (including
            its ``category_id`` group-by context, PE/RA/RR/Windup &
            Reporting) and that its domain, searched, matches the
            contributing worksheets
        """
        audit = self._create_general_audit_for_source_worksheets("Source Worksheets")
        other_audit = self._create_general_audit_for_source_worksheets(
            "Source Worksheets - Other Engagement"
        )
        ws_type_a8c54f3 = self.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_a8c54f3"
        )
        ws_type_b66777d = self.env.ref(
            "ssi_general_audit_worksheet_final_report.worksheet_type_b66777d"
        )
        # general_audit_worksheet_mixin._check_unique_general_audit()
        # rejects a second record sharing (general_audit_id, type_id)
        # unless that type's allowed_audit=True (worksheet_type_a8c54f3
        # is not). review_worksheet and the "different employee"
        # worksheet below need their OWN distinct type_id -- of the
        # SAME model_name -- so they can coexist with prep_worksheet on
        # the same "audit".
        WorksheetType = self.env["general_audit_worksheet_type"]
        ws_type_a8c54f3_review = WorksheetType.create(
            {
                "name": "Test Type - Source Worksheets Review",
                "code": "/",
                "model_name": "general_audit_ws_a8c54f3",
            }
        )
        ws_type_a8c54f3_other_employee = WorksheetType.create(
            {
                "name": "Test Type - Source Worksheets Other Employee",
                "code": "/",
                "model_name": "general_audit_ws_a8c54f3",
            }
        )

        member_user = self.env["res.users"].create(
            {
                "name": "Source Worksheets Test User",
                "login": "source_worksheets_test_user@example.com",
                "email": "source_worksheets_test_user@example.com",
            }
        )
        member_employee = self.env["hr.employee"].create(
            {
                "name": "Test Team Member - Source Worksheets",
                "user_id": member_user.id,
            }
        )
        other_user = self.env["res.users"].create(
            {
                "name": "Source Worksheets Other User",
                "login": "source_worksheets_other_user@example.com",
                "email": "source_worksheets_other_user@example.com",
            }
        )

        b66777d_worksheet = self.env["general_audit_ws_b66777d"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type_b66777d.id,
            }
        )

        prep_worksheet = self.env["general_audit_ws_a8c54f3"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type_a8c54f3.id,
                "user_id": member_user.id,
                "preparation_time": 4,
            }
        )
        review_worksheet = self.env["general_audit_ws_a8c54f3"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type_a8c54f3_review.id,
            }
        )
        review_worksheet.write({"reviewer_id": member_user.id, "review_time": 6})
        # Same engagement, contributed by a DIFFERENT employee -- must
        # be excluded from the row's source worksheets.
        self.env["general_audit_ws_a8c54f3"].create(
            {
                "general_audit_id": audit.id,
                "type_id": ws_type_a8c54f3_other_employee.id,
                "user_id": other_user.id,
                "preparation_time": 2,
            }
        )
        # Same employee, but a DIFFERENT engagement -- must also be
        # excluded.
        self.env["general_audit_ws_a8c54f3"].create(
            {
                "general_audit_id": other_audit.id,
                "type_id": ws_type_a8c54f3.id,
                "user_id": member_user.id,
                "preparation_time": 9,
            }
        )

        row = self.env["general_audit_ws_b66777d.team_allocation"].create(
            {
                "worksheet_id": b66777d_worksheet.id,
                "team_id": member_employee.id,
                "pe_allocation": 10,
            }
        )

        action = row.action_view_source_worksheets()

        self.assertEqual(action["res_model"], "general_audit_worksheet")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["context"], {"group_by": "category_id"})

        found = self.env["general_audit_worksheet"].search(action["domain"])
        self.assertEqual(
            set(found.ids),
            {
                prep_worksheet.worksheet_id.id,
                review_worksheet.worksheet_id.id,
            },
        )
