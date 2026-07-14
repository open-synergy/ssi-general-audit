# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestGeneralAuditWSRomm(YamlTransactionCase):
    def test_general_audit_ws_romm(self):
        self.run_yaml_scenario("test_data_general_audit_ws_romm.yaml")

    def test_onchange_type_id_sets_parent_type_id_d66d87a(self):
        """``type_id`` is fixed per concrete worksheet (``_default_type_id``
        resolves it from ``_type_xml_id``) and is rendered read-only in the
        standard form view except while ``draft``, so a brand-new record is
        the only state where the Form API loads it. The onchange still
        fires for that defaulted value while the Form loads the new record,
        which is what this asserts: ``parent_type_id`` mirrors ``type_id``
        without any explicit assignment being possible.

        Mirrors ``ssi_general_audit_worksheet_planning_memorandum/tests/
        test_general_audit_ws_fbbe0f8.py::
        test_onchange_type_id_sets_parent_type_id`` for the same mixin
        onchange (``onchange_parent_type_id`` on
        ``general_audit_worksheet_mixin``). Deliberately not using
        ``with Form(...) as form:`` — the context manager calls ``save()``
        on ``__exit__``, which would fail here because ``general_audit_id``
        (a real required field) is never filled; this test only cares about
        the pending onchange state.

        This is also not expressed as a YAML ``action: form`` scenario on
        purpose: per this repo's unit-test conventions, ``action: form``
        must never carry an inline ``assert`` inside its ``ops:`` list (a
        documented bug in ``odoo_yaml_test``'s ``Form`` proxy —
        ``hasattr(form, "__len__")`` raises ``AssertionError`` instead of
        ``AttributeError`` for fields the concrete view does not expose),
        and ``type_id`` is exactly such a not-writable-from-a-generic-form
        field here.
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_romm.worksheet_type_d66d87a"
        )
        form = Form(self.env["general_audit_ws_d66d87a"])
        self.assertEqual(form.type_id, ws_type)
        self.assertEqual(form.parent_type_id, ws_type)
