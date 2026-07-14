# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestWSA418D89(YamlTransactionCase):
    def test_ws_a418d89(self):
        self.run_yaml_scenario("test_data_ws_a418d89.yaml")

    def test_onchange_type_id_updates_parent_type_id(self):
        """``onchange_parent_type_id`` (``general_audit_worksheet_mixin``) is
        declared ``@api.onchange("type_id")`` and only fires through the Form
        API, not through plain ``.create()``/``.write()`` — so it cannot be
        expressed as a YAML ``create``/``write`` step. Exercised here directly
        against a new, unsaved ``general_audit_ws_a418d89`` Form."""
        type_c16abd7 = self.env.ref(
            "ssi_general_audit_worksheet_inherent_risk.worksheet_type_c16abd7"
        )
        form = Form(self.env["general_audit_ws_a418d89"])
        form.type_id = type_c16abd7
        self.assertEqual(form.parent_type_id, type_c16abd7)
