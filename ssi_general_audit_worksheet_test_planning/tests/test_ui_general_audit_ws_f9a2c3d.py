# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class"), and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


def _create_worksheet(env, load_detail):
    """Create an open Test of Detail Planning worksheet with one account.

    ``user_id`` is explicit throughout: ``env`` runs as SUPERUSER, and the
    record rule of the worksheet would otherwise hide these fixtures from
    the admin session of the tour (structure-and-runner.md "Fixture
    setUpClass berjalan sebagai SUPERUSER").

    :param env: the environment of the test class
    :param load_detail: press the Detail button before returning
    :return: the worksheet created
    """
    admin = env.ref("base.user_admin")
    env["ir.config_parameter"].sudo().set_param(
        "ssi_general_audit.max_number_of_cpa_license", "100"
    )
    client = (
        env["res.partner"]
        .with_user(admin)
        .create({"name": "Test Audit Client - F9A2C3D Tour", "is_company": True})
    )
    accountant = (
        env["res.partner"]
        .with_user(admin)
        .create({"name": "Test Audit Accountant - F9A2C3D Tour"})
    )
    env["res.partner.id_number"].with_user(admin).create(
        {
            "partner_id": accountant.id,
            "category_id": env.ref(
                "ssi_partner_identification_cpa_license"
                ".partner_identification_accountant_cpa_license"
            ).id,
            "name": "CPA-F9A2C3D-TOUR-0001",
        }
    )
    account_type_set = (
        env["client_account_type_set"]
        .with_user(admin)
        .create({"name": "Test Account Type Set - F9A2C3D Tour", "code": "/"})
    )
    standard = (
        env["accountant.financial_accounting_standard"]
        .with_user(admin)
        .create({"name": "Test Standard - F9A2C3D Tour", "code": "/"})
    )
    audit = (
        env["general_audit"]
        .with_user(admin)
        .create(
            {
                "title": "Test General Audit - F9A2C3D Tour",
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
        .create({"name": "Test Account Group - F9A2C3D Tour", "code": "/"})
    )
    account_type = (
        env["client_account_type"]
        .with_user(admin)
        .create(
            {
                # Unique name asserted by the tour once the line is loaded.
                "name": "TOUR-F9A2C3D-TYPE",
                "code": "/",
                "group_id": account_group.id,
                "normal_balance": "dr",
                # The default python_code reads a field that
                # general_audit.standard_detail does not have.
                "python_code": "result = 0.0",
            }
        )
    )
    env["general_audit.standard_detail"].with_user(admin).create(
        {"general_audit_id": audit.id, "type_id": account_type.id}
    )
    worksheet = (
        env["general_audit_ws_f9a2c3d"]
        .with_user(admin)
        .create(
            {
                "general_audit_id": audit.id,
                "type_id": env.ref(
                    "ssi_general_audit_worksheet_test_planning.worksheet_type_f9a2c3d"
                ).id,
            }
        )
    )
    worksheet.with_user(admin).action_open()
    if load_detail:
        worksheet.with_user(admin).action_load_detail()
    worksheet.invalidate_cache()
    return worksheet


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsF9a2c3dLoadDetail(HttpSavepointCase):
    """Tour test for the Detail button of ``general_audit_ws_f9a2c3d``."""

    @classmethod
    def setUpClass(cls):
        """Create an open worksheet whose lines are not loaded yet.

        The Pre-Condition is prepared here in Python; the tour only
        exercises opening the worksheet and clicking Detail.
        """
        super().setUpClass()
        cls.worksheet = _create_worksheet(cls.env, load_detail=False)

    def test_load_detail(self):
        """Run the Detail tour for ``general_audit_ws_f9a2c3d``.

        Covers the line created for the account and the nine columns of
        the Details table.

        IK: docs/general_audit_ws_f9a2c3d/01-load-detail.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_test_planning_f9a2c3d_load_detail",
            login="admin",
        )


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsF9a2c3dFillPlanning(HttpSavepointCase):
    """Tour test for the planning columns of ``general_audit_ws_f9a2c3d``."""

    @classmethod
    def setUpClass(cls):
        """Create an open worksheet whose lines are already loaded.

        The Pre-Condition is prepared here in Python; the tour only
        exercises choosing the timing, the extent and the techniques.
        """
        super().setUpClass()
        cls.worksheet = _create_worksheet(cls.env, load_detail=True)

    def test_fill_planning(self):
        """Run the planning tour for ``general_audit_ws_f9a2c3d``.

        Covers choosing Timing, Extent and two Primary Audit Techniques.

        IK: docs/general_audit_ws_f9a2c3d/02-isi-perencanaan.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_test_planning_f9a2c3d_fill_planning",
            login="admin",
        )
