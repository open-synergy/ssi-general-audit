# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestGeneralAuditWSfbbe0f8(YamlTransactionCase):
    def test_general_audit_ws_fbbe0f8(self):
        self.run_yaml_scenario("test_data_general_audit_ws_fbbe0f8.yaml")

    def test_onchange_type_id_sets_parent_type_id(self):
        """``type_id`` is fixed per concrete worksheet (``_default_type_id``
        resolves it from ``_type_xml_id``) and is rendered read-only in the
        standard form view, so it can never be reassigned through the Form
        API. The onchange still fires for that defaulted value while the
        Form loads a brand-new record, which is what this asserts:
        ``parent_type_id`` mirrors ``type_id`` without any explicit
        assignment being possible.

        Pattern mirrors ``ssi_general_audit_worksheet_expert/tests/
        test_ws_bab9d32.py::test_onchange_type_id_sets_parent_type_id`` for
        the same mixin onchange (``onchange_parent_type_id`` on
        ``general_audit_worksheet_mixin``). Deliberately not using
        ``with Form(...) as form:`` — the context manager calls ``save()``
        on ``__exit__``, which would fail here because ``general_audit_id``
        (a real required field) is never filled; this test only cares about
        the pending onchange state.

        This is also not expressed as a YAML ``action: form`` scenario on
        purpose: per this repo's unit-test conventions, ``action: form``
        must never carry an inline ``assert`` inside its ``ops:`` list
        (a documented bug in ``odoo_yaml_test``'s ``Form`` proxy —
        ``hasattr(form, "__len__")`` raises ``AssertionError`` instead of
        ``AttributeError`` for fields the concrete view does not expose),
        and ``type_id`` is exactly such a not-writable-from-a-generic-form
        field here.
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_planning_memorandum.worksheet_type_fbbe0f8"
        )
        form = Form(self.env["general_audit_ws_fbbe0f8"])
        self.assertEqual(form.type_id, ws_type)
        self.assertEqual(form.parent_type_id, ws_type)

    def test_get_dynamic_labels_cache_invalidation(self):
        """``general_audit_ws_fbbe0f8.get_dynamic_labels()`` is decorated
        with ``@api.model`` + ``functools.lru_cache()`` — a cache stored on
        the Python function object itself, shared across every recordset
        and even across otherwise-unrelated test transactions in this
        process (see ``ssi_general_audit/tests/README_FIXTURE.md`` and the
        docstring on ``general_audit_ws_a753ab9.item``).
        ``general_audit_ws_a753ab9.item.create()``/``write()``/``unlink()``
        each call ``.cache_clear()`` explicitly to keep it fresh; this test
        proves that wiring actually works for all three operations.

        Written directly in Python (not YAML) because ``action: call`` in
        ``odoo_yaml_test`` discards the method's return value — it only
        supports asserting *fields on the target record* afterwards, never
        the return value of the call itself, and there is no YAML action
        that captures an arbitrary Python return value (here, a plain
        ``dict``) into the scenario registry. Testing the cached dict's
        content genuinely requires calling the method directly and
        inspecting what it returns.

        Uses a field-name probe (``x_test_probe_field``) that does not
        collide with the ``related_field`` values already shipped as
        mandatory (non-demo) data in
        ``data/master/general_audit_ws_a753ab9_item.xml`` (e.g.
        ``financial_accounting_standard_id``, ``other_report_ids``, ...),
        so the assertions only care about *our* probe key, regardless of
        whatever those shipped items already populated in the shared cache.
        """
        Item = self.env["general_audit_ws_a753ab9.item"]
        Worksheet = self.env["general_audit_ws_fbbe0f8"]
        option_set = self.env.ref("ssi_general_audit.checklist_option_set_1")

        labels = Worksheet.get_dynamic_labels()
        self.assertNotIn("x_test_probe_field", labels)

        item = Item.create(
            {
                "name": "Cache probe item - create",
                "checklist_type": "characteristic",
                "option_set_id": option_set.id,
                "related_field": "x_test_probe_field",
            }
        )
        labels = Worksheet.get_dynamic_labels()
        self.assertEqual(labels.get("x_test_probe_field"), "Cache probe item - create")

        item.write({"name": "Cache probe item - written"})
        labels = Worksheet.get_dynamic_labels()
        self.assertEqual(labels.get("x_test_probe_field"), "Cache probe item - written")

        item.unlink()
        labels = Worksheet.get_dynamic_labels()
        self.assertNotIn("x_test_probe_field", labels)
