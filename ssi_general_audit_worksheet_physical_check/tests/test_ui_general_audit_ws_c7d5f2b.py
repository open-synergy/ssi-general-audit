# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsC7D5F2B(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_c7d5f2b`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the engagement, GL sources, Sample Determination, worksheet.

        Everything the tour itself is meant to exercise (Data Mode,
        General Ledger, Data Source, Sample Determination, Reference
        Column Number, the Data Comparison line, the Check line, and
        the Compute Check Data click) is left blank/default here -- the
        tour fills those in through the UI. The Pre-Condition (an Open
        worksheet linked to an engagement with two General Ledger
        worksheets and a matching Sample Determination worksheet
        already imported) is prepared in Python.
        """
        super().setUpClass()
        # user_id is explicit throughout: cls.env runs as SUPERUSER, and
        # the record rule general_audit_ws_c7d5f2b_internal_user_rule
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
            .create({"name": "Test Audit Client - C7D5F2B Tour", "is_company": True})
        )
        accountant = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Test Audit Accountant - C7D5F2B Tour"})
        )
        cpa_category = cls.env.ref(
            "ssi_partner_identification_cpa_license"
            ".partner_identification_accountant_cpa_license"
        )
        cls.env["res.partner.id_number"].with_user(cls.admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-C7D5F2B-TOUR-0001",
            }
        )
        account_type_set = (
            cls.env["client_account_type_set"]
            .with_user(cls.admin)
            .create({"name": "Test Account Type Set - C7D5F2B Tour", "code": "/"})
        )
        standard = (
            cls.env["accountant.financial_accounting_standard"]
            .with_user(cls.admin)
            .create({"name": "Test Standard - C7D5F2B Tour", "code": "/"})
        )
        audit = (
            cls.env["general_audit"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Test General Audit - C7D5F2B Tour",
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
        # Reference/population source. The tour picks this GL
        # POSITIONALLY (first created, sorts first under the model's
        # _order "general_audit_id, parent_type_id, id" since both GL
        # fixtures share general_audit_id/parent_type_id) -- NOT by
        # typing a "title", because display_name here is the
        # worksheet's own document number (mixin_transaction
        # name_get: record.name, or "*"+id while name == "/"), not the
        # "title" field. "title" is also a related field onto
        # general_audit_id.title (ssi_general_audit
        # general_audit_worksheet.py), so setting it here would rename
        # the ENGAGEMENT's title, not label this worksheet -- left at
        # its own default instead.
        cls.ref_gl = (
            cls.env["general_audit_ws_d209914"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_d209914.id,
                    "raw_data": "Ref,Amount\nTOUR-C7D5F2B-R1,1000\n",
                }
            )
        )
        # Comparison source, selected on the Data Comparison line.
        # Created SECOND on purpose -- the tour picks it positionally
        # as the second option, right after ref_gl.
        cls.cmp_gl = (
            cls.env["general_audit_ws_d209914"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_d209914.id,
                    "raw_data": "Ref,Amount\nTOUR-C7D5F2B-R1,1000\n",
                }
            )
        )

        ws_type_a916660 = cls.env.ref(
            "ssi_general_audit_worksheet_sample_determination.worksheet_type_a916660"
        )
        # general_ledger_id (with data_mode="gl") must be set to ref_gl so
        # this Sample Determination is picked up by
        # _compute_allowed_sample_determination_ids on the worksheet
        # (domain-filtered in the UI, unlike a direct ORM write), and its
        # own raw_data (a compute field mirroring the Data Mode pattern)
        # ends up equal to ref_gl.raw_data.
        cls.sd = (
            cls.env["general_audit_ws_a916660"]
            .with_user(cls.admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type_a916660.id,
                    "data_mode": "gl",
                    "general_ledger_id": cls.ref_gl.id,
                    "sampling_data": "No,Ref\n1,TOUR-C7D5F2B-R1\n",
                }
            )
        )

        ws_type = cls.env.ref(
            "ssi_general_audit_worksheet_physical_check.worksheet_type_c7d5f2b"
        )
        cls.worksheet = (
            cls.env["general_audit_ws_c7d5f2b"]
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

    def test_fill_data_comparison(self):
        """Run the fill-Data/Data Comparison/Check tour for c7d5f2b.

        IK: docs/general_audit_ws_c7d5f2b/01-isi-data-perbandingan.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_physical_check_c7d5f2b_fill_data_comparison",
            login="admin",
        )
