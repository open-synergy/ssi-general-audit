# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_general_audit_worksheet_final_report"


@tagged("post_install", "-at_install")
class TestMigration14015(YamlTransactionCase):
    """Conclusion source clean-up of migration 14.0.1.15.0."""

    def test_conclusion_source_data(self):
        """Run the installed conclusion source YAML scenario."""
        self.run_yaml_scenario("test_data_ws_a8c54f3_conclusion_source.yaml")

    def _load_script(self):
        """Load the post-migration script from its file.

        :return: the imported script module
        """
        path = os.path.join(
            get_module_path(MODULE),
            "migrations",
            "14.0.1.15.0",
            "post-migration.py",
        )
        spec = importlib.util.spec_from_file_location("post_migrate_1_15_0", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_migration_unlinks_sources_and_keeps_typed_lines(self):
        """Unlink removed sources and delete only non typed lines.

        Python-only test, trigger P10 (limitation L-11): the migration
        script must be imported from its file, which ``EVAL:`` cannot do.
        The scenario links the General Ledger type back as a source, then
        checks the script unlinks it again and is idempotent. The
        function is called with the cursor, as the decorator expects.
        """
        memo_type = self.env.ref(f"{MODULE}.worksheet_type_a8c54f3")
        gl_type = self.env.ref(
            "ssi_general_audit_worksheet_client_package.worksheet_type_d209914"
        )
        other_type = self.env.ref(
            "ssi_general_audit_worksheet_final_materiality.worksheet_type_bb33b94"
        )
        memo_type.write({"conclusion_source_type_ids": [(4, gl_type.id)]})
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.15.0")
        memo_type.invalidate_cache()
        self.assertNotIn(gl_type, memo_type.conclusion_source_type_ids)
        self.assertIn(other_type, memo_type.conclusion_source_type_ids)
        script.migrate(self.env.cr, "14.0.1.15.0")
        memo_type.invalidate_cache()
        self.assertNotIn(gl_type, memo_type.conclusion_source_type_ids)
