# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestMasterData(YamlTransactionCase):
    def test_master_data(self):
        self.run_yaml_scenario("test_data_master_data.yaml")

    def test_general_audit_fraud_factor_category_id_required(self):
        """``category_id`` is declared ``required=True`` directly on the
        field (``models/master/general_audit_fraud_factor.py``), so Odoo
        enforces it with a database-level ``NOT NULL`` constraint rather
        than an ``@api.constrains``/``UserError``. Omitting it from
        ``create()`` therefore raises a raw ``psycopg2.IntegrityError`` --
        not one of the exception types ``odoo_yaml_test``'s
        ``expect_error`` can name (its whitelist is a fixed set of Python
        builtins plus ``odoo.exceptions`` classes; ``psycopg2.IntegrityError``
        is in neither -- see
        ``ssi_general_audit_worksheet_population/tests/test_general_audit_ws_a01723b.py``
        method ``test_population_type_id_required`` for the same pattern).
        This is exactly the documented exception to "assert negative paths
        with expect_error in YAML" -- there is no YAML-expressible way to
        assert this one, hence the (otherwise discouraged) Python
        ``assertRaises``.
        """
        admin = self.env.ref("base.user_admin")

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["general_audit_fraud_factor"].with_user(admin).create(
                        {
                            "name": "Test Fraud Factor - Required Field",
                            "code": "/",
                            # category_id intentionally omitted
                        }
                    )

    def test_general_audit_going_concern_category_id_required(self):
        """Same reasoning as
        ``test_general_audit_fraud_factor_category_id_required`` above:
        ``category_id`` on ``general_audit_going_concern``
        (``models/master/general_audit_going_concern.py``) is
        ``required=True`` directly on the field, so omitting it raises a
        raw ``psycopg2.IntegrityError`` rather than a
        ``ValidationError``/``UserError`` expressible via ``expect_error``.
        """
        admin = self.env.ref("base.user_admin")

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(IntegrityError):
                with self.cr.savepoint():
                    self.env["general_audit_going_concern"].with_user(admin).create(
                        {
                            "name": "Test Going Concern - Required Field",
                            "code": "/",
                            # category_id intentionally omitted
                        }
                    )
