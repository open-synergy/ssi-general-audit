# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_general_audit_worksheet_client_package"


@tagged("post_install", "-at_install")
class TestMigration14017(YamlTransactionCase):
    """Sort key rebuild of migration 14.0.1.7.0."""

    def setUp(self):
        """Create one item of each Others type with the same number."""
        super().setUp()
        item_model = self.env["general_audit_data_collection"]
        category = self.env["general_audit_data_collection_category"].create(
            {"name": "Test Category - Migration", "code": "/"}
        )
        self.permanent = item_model.create(
            {
                "name": "Migration permanent",
                "code": "ZP-2",
                "type": "permanent_file",
                "category_id": category.id,
            }
        )
        self.current = item_model.create(
            {
                "name": "Migration current",
                "code": "ZC-2",
                "type": "current_file",
                "category_id": category.id,
            }
        )

    def _load_script(self):
        """Load the post-migration script from its file.

        :return: the imported script module
        """
        path = os.path.join(
            get_module_path(MODULE),
            "migrations",
            "14.0.1.7.0",
            "post-migrate.py",
        )
        spec = importlib.util.spec_from_file_location("post_migrate_1_7_0", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_permanent_file_sorts_before_current_file(self):
        """Sort Permanent File items before Current File items.

        Python-only test, trigger P10 (limitation L-11): the order of
        the records returned by ``search`` cannot be asserted in a YAML
        scenario. The line models sort on the same stored key.
        """
        items = self.env["general_audit_data_collection"].search(
            [("id", "in", (self.permanent | self.current).ids)],
            order="code_sort, id",
        )
        self.assertEqual(items, self.permanent | self.current)

    def test_migration_rebuilds_sort_key(self):
        """Rebuild a stale sort key and stay idempotent.

        Python-only test, trigger P10 (limitation L-11): the migration
        script must be imported from its file, which ``EVAL:`` cannot do.
        The stale key is written through SQL, as an old database holds
        it, then the script is called with the cursor, as the decorator
        expects.
        """
        stale = "Z-00000002"
        self.env.cr.execute(
            "UPDATE general_audit_data_collection SET code_sort = %s WHERE id IN %s",
            (stale, tuple((self.permanent | self.current).ids)),
        )
        self.permanent.invalidate_cache()
        self.assertEqual(self.permanent.code_sort, stale)
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.7.0")
        self.permanent.invalidate_cache()
        self.current.invalidate_cache()
        self.assertEqual(self.permanent.code_sort, "1ZP-00000002")
        self.assertEqual(self.current.code_sort, "2ZC-00000002")
        script.migrate(self.env.cr, "14.0.1.7.0")
        self.permanent.invalidate_cache()
        self.assertEqual(self.permanent.code_sort, "1ZP-00000002")
