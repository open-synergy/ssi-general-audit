# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestWSBab9d32(YamlTransactionCase):
    def test_ws_bab9d32(self):
        self.run_yaml_scenario("test_data_ws_bab9d32.yaml")

    def test_onchange_type_id_sets_parent_type_id(self):
        """``type_id`` is fixed per concrete worksheet (``_default_type_id``
        resolves it from ``_type_xml_id``) and is rendered read-only in the
        standard form view, so it can never be reassigned through the Form
        API. The onchange still fires for that defaulted value while the
        Form loads a brand-new record, which is what this asserts:
        ``parent_type_id`` mirrors ``type_id`` without any explicit
        assignment being possible.

        Deliberately not using ``with Form(...) as form:`` — the context
        manager calls ``save()`` on ``__exit__``, which would fail here
        because ``general_audit_id`` (a real required field) is never
        filled; this test only cares about the pending onchange state.
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_expert.worksheet_type_bab9d32"
        )
        form = Form(self.env["general_audit_ws_bab9d32"])
        self.assertEqual(form.type_id, ws_type)
        self.assertEqual(form.parent_type_id, ws_type)
