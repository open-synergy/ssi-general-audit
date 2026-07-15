# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestWSAe48e68(YamlTransactionCase):
    def test_ws_ae48e68(self):
        self.run_yaml_scenario("test_data_ws_ae48e68.yaml")

    def test_onchange_type_id_set_parent_type(self):
        """``type_id`` is fixed per concrete worksheet (``_default_type_id``
        resolves it from ``_type_xml_id``) and is rendered read-only in the
        standard form view except while ``draft``, so a brand-new record is
        the only state where the Form API loads it. The onchange still
        fires for that defaulted value while the Form loads the new record,
        which is what this asserts: ``parent_type_id`` mirrors ``type_id``
        without any explicit assignment being possible.

        Mirrors ``ssi_general_audit_worksheet_romm/tests/
        test_general_audit_ws_romm.py::
        test_onchange_type_id_sets_parent_type_id_d66d87a`` and
        ``ssi_general_audit_worksheet_specific_procedure/tests/
        test_general_audit_ws_specific_procedure.py::
        test_onchange_type_id_set_parent_type_id`` for the same mixin
        onchange (``onchange_parent_type_id`` on
        ``general_audit_worksheet_mixin``). Deliberately not expressed as a
        YAML ``action: form`` scenario: per this repo's unit test
        conventions, ``action: form`` must never carry an inline ``assert``
        inside its ``ops:`` list (a documented bug in ``odoo_yaml_test``'s
        ``Form`` proxy), and ``type_id`` is exactly such a
        not-writable-from-a-generic-form field here (readonly except in
        ``draft``, so only a brand new, unsaved record ever exposes it).
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_external_communication.worksheet_type_ae48e68"
        )
        form = Form(self.env["general_audit_ws_ae48e68"])
        self.assertEqual(form.type_id, ws_type)
        self.assertEqual(form.parent_type_id, ws_type)
