# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

from ..hooks import WORKSHEET_TYPE_XMLID, uninstall_hook
from .ui_fixture import create_open_general_audit


@tagged("post_install", "-at_install")
class TestUninstallHook(YamlTransactionCase):
    """Check ``uninstall_hook`` by calling it directly as a function."""

    def setUp(self):
        """Create an audit, a foreign type and the references to them."""
        super().setUp()
        env = self.env
        self.population = env.ref(WORKSHEET_TYPE_XMLID)
        self.other = env["general_audit_worksheet_type"].search(
            [("id", "!=", self.population.id)], limit=1
        )
        self.audit = create_open_general_audit(env, "UNINSTALL-HOOK")
        self.audit.write(
            {
                "additional_worksheet_type_ids": [
                    (4, self.population.id),
                    (4, self.other.id),
                ],
                "required_worksheet_type_ids": [
                    (4, self.population.id),
                    (4, self.other.id),
                ],
            }
        )
        summary = env["general_audit.worksheet_summary"]
        self.population_summary = summary.create(
            {
                "general_audit_id": self.audit.id,
                "type_id": self.population.id,
            }
        )
        self.other_summary = summary.create(
            {"general_audit_id": self.audit.id, "type_id": self.other.id}
        )

    def _run_hook(self):
        """Call the hook the way ``odoo.modules.loading`` does."""
        uninstall_hook(self.env.cr, self.env.registry)
        self.env.clear()

    def test_removes_type_and_references(self):
        """Assert the type and all references to it disappear.

        Pure Python - trigger P10 (L-09: the hook is a plain function).
        """
        population_id = self.population.id
        self._run_hook()
        self.assertFalse(
            self.env["general_audit_worksheet_type"].browse(population_id).exists()
        )
        self.assertFalse(self.population_summary.exists())
        self.assertNotIn(population_id, self.audit.additional_worksheet_type_ids.ids)
        self.assertNotIn(population_id, self.audit.required_worksheet_type_ids.ids)

    def test_keeps_other_types(self):
        """Assert other types and their references stay untouched.

        Pure Python - trigger P10 (L-09: the hook is a plain function).
        """
        self._run_hook()
        self.assertTrue(self.other.exists())
        self.assertTrue(self.other_summary.exists())
        self.assertIn(self.other, self.audit.additional_worksheet_type_ids)
        self.assertIn(self.other, self.audit.required_worksheet_type_ids)
        self.assertTrue(self.audit.exists())

    def test_idempotent(self):
        """Assert running the hook twice does not fail.

        Pure Python - trigger P10 (L-09: the hook is a plain function).
        """
        self._run_hook()
        self._run_hook()
