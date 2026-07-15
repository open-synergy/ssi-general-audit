# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from datetime import date

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestGeneralAuditWSa01723b(YamlTransactionCase):
    def test_general_audit_ws_a01723b(self):
        self.run_yaml_scenario("test_data_general_audit_ws_a01723b.yaml")

    def test_population_type_id_required(self):
        """``population_type_id`` is declared ``required=True`` directly on
        the field (``models/a01723b/general_audit_ws_a01723b.py``), so Odoo
        enforces it with a database-level ``NOT NULL`` constraint rather
        than an ``@api.constrains``/``UserError``. Omitting it from
        ``create()`` therefore raises a raw ``psycopg2.IntegrityError`` --
        not one of the exception types ``odoo_yaml_test``'s
        ``expect_error`` can name (its whitelist is a fixed set of Python
        builtins plus ``odoo.exceptions`` classes; see
        ``odoo_yaml_test.case._STDLIB_ERRORS`` / ``_ODOO_ERROR_NAMES`` --
        ``psycopg2.IntegrityError`` is in neither). Odoo core's own test
        suite hits the same wall for the same reason (see e.g.
        ``odoo/addons/hr_holidays/tests/test_holidays_flow.py``, which
        comments "# No ValidationError" next to an identical
        ``assertRaises(IntegrityError)``). This is exactly the documented
        exception to "assert negative paths with expect_error in YAML" --
        there is no YAML-expressible way to assert this one, hence the
        (otherwise discouraged) Python ``assertRaises``.
        """
        admin = self.env.ref("base.user_admin")
        self.env["ir.config_parameter"].sudo().set_param(
            "ssi_general_audit.max_number_of_cpa_license", "100"
        )
        client = (
            self.env["res.partner"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Audit Client - Required Field",
                    "is_company": True,
                }
            )
        )
        accountant = (
            self.env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - Required Field"})
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-POP-REQ-0001",
            }
        )
        account_type_set = (
            self.env["client_account_type_set"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Account Type Set - Required Field",
                    "code": "/",
                }
            )
        )
        standard = (
            self.env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Financial Accounting Standard - Required Field",
                    "code": "/",
                }
            )
        )
        audit = (
            self.env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - Required Field",
                    "partner_id": client.id,
                    "accountant_id": accountant.id,
                    "account_type_set_id": account_type_set.id,
                    "financial_accounting_standard_id": standard.id,
                    "date_start": date(2026, 1, 1),
                    "date_end": date(2026, 12, 31),
                    "need_interim": False,
                    "need_previous": False,
                    "num_of_consecutive_audit_firm": 1,
                    "num_of_consecutive_audit_accountant": 1,
                }
            )
        )
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_population.worksheet_type_a01723b"
        )

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["general_audit_ws_a01723b"].with_user(admin).create(
                        {
                            "general_audit_id": audit.id,
                            "type_id": ws_type.id,
                            # population_type_id intentionally omitted
                        }
                    )
