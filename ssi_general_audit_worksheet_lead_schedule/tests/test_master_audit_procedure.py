# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestMasterAuditProcedure(YamlTransactionCase):
    def test_master_audit_procedure(self):
        self.run_yaml_scenario("test_data_master_audit_procedure.yaml")

    def test_onchange_account_type_id_clears_category(self):
        """Form() test for ``onchange_category_id``.

        Not expressed as a YAML scenario: ``action: form`` combined with an
        inline ``ops: [..., {assert: ...}]`` step crashes with
        ``AssertionError: __len__ was not found in the view`` -- a bug in
        the installed ``odoo_yaml_test`` library, not in this module.
        ``_read_path()`` calls ``hasattr(current, "__len__")`` on the live
        Form proxy before reading any field; Odoo's ``Form.__getattr__``
        (``odoo/tests/common.py``) raises ``AssertionError`` (not
        ``AttributeError``) for any attribute absent from the view's field
        list, and Python's ``hasattr()`` only swallows ``AttributeError``,
        so the ``AssertionError`` propagates and aborts the step. Saving the
        form afterwards is not an option either: ``category_id`` is
        ``required=True`` on ``general_audit_audit_procedure`` and the
        onchange leaves it empty, so ``form.save()`` would fail on the
        missing required field. A direct ``Form()`` call is the only way
        left to exercise this onchange.
        """
        account_group = self.env["client_account_group"].create(
            {"name": "Test Account Group - Onchange", "code": "/"}
        )
        account_type_a = self.env["client_account_type"].create(
            {
                "name": "Test Account Type A - Onchange",
                "code": "/",
                "group_id": account_group.id,
                "normal_balance": "dr",
                "python_code": "result = 0.0",
            }
        )
        account_type_b = self.env["client_account_type"].create(
            {
                "name": "Test Account Type B - Onchange",
                "code": "/",
                "group_id": account_group.id,
                "normal_balance": "cr",
                "python_code": "result = 0.0",
            }
        )
        assertion_type = self.env["general_audit_assersion_type"].create(
            {"name": "Existence", "code": "/"}
        )
        category_a = self.env["general_audit_audit_procedure_category"].create(
            {
                "name": "Existence and Occurrence - Type A (onchange)",
                "code": "/",
                "account_type_id": account_type_a.id,
                "assertion_type_ids": [(6, 0, assertion_type.ids)],
            }
        )

        form = Form(self.env["general_audit_audit_procedure"])
        form.account_type_id = account_type_a
        form.category_id = category_a
        form.account_type_id = account_type_b

        self.assertFalse(form.category_id)
