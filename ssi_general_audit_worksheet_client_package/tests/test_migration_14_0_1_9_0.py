# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

from .ui_fixture import create_populate_worksheet

MODULE = "ssi_general_audit_worksheet_client_package"


@tagged("post_install", "-at_install")
class TestMigration14019(YamlTransactionCase):
    """Move of the reporting timetable lines by migration 14.0.1.9.0."""

    def setUp(self):
        """Create a worksheet and rebuild the old timetable layout.

        A fresh database does not have the columns and the attachment
        relation of the old reporting timetable, so they are added
        through SQL. The test transaction rolls them back.
        """
        super().setUp()
        self.worksheet = create_populate_worksheet(self.env, "F5A3CEE-MIGRATION")
        self.master = self.env["general_audit_data_collection"].search(
            [("code", "=", "0-TOUR-PF")], limit=1
        )
        self.attachment = self.env["ir.attachment"].create(
            {
                "name": "Old timetable evidence",
                "type": "url",
                "url": "https://example.com/old-timetable",
                "res_model": "general_audit_ws_f5a3cee",
                "res_id": self.worksheet.id,
            }
        )
        self.env["base"].flush()
        self.env.cr.execute(
            """
            ALTER TABLE general_audit_ws_f5a3cee_reporting_timetable
                ADD COLUMN data_collection_id integer,
                ADD COLUMN category_id integer,
                ADD COLUMN complete_ok boolean;
            CREATE TABLE rel_ga_f5a3cee_reporting_timetable_2_attachment (
                f5a3cee_reporting_timetable_id integer NOT NULL,
                attachment_id integer NOT NULL
            );
            """
        )
        self.master_line_id = self._insert_old_line(
            "Old master line",
            "2026-06-30",
            True,
            self.master.id,
            self.master.category_id.id,
        )
        self.manual_line_id = self._insert_old_line(
            "Old manual line", None, False, None, None
        )
        self.env.cr.execute(
            """
            INSERT INTO rel_ga_f5a3cee_reporting_timetable_2_attachment
            VALUES (%s, %s)
            """,
            (self.master_line_id, self.attachment.id),
        )

    def _insert_old_line(self, description, date, complete_ok, master_id, categ_id):
        """Insert one line with the old reporting timetable layout.

        :param str description: description of the line
        :param str date: date of the line, or ``None``
        :param bool complete_ok: completion flag of the line
        :param int master_id: Data Collection item, or ``None``
        :param int categ_id: category, or ``None``
        :return: id of the new line
        :rtype: int
        """
        self.env.cr.execute(
            """
            INSERT INTO general_audit_ws_f5a3cee_reporting_timetable
                (worksheet_id, description, date, complete_ok,
                 data_collection_id, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                self.worksheet.id,
                description,
                date,
                complete_ok,
                master_id,
                categ_id,
            ),
        )
        return self.env.cr.fetchone()[0]

    def _load_script(self):
        """Load the post-migration script from its file.

        :return: the imported script module
        """
        path = os.path.join(
            get_module_path(MODULE),
            "migrations",
            "14.0.1.9.0",
            "post-migrate.py",
        )
        spec = importlib.util.spec_from_file_location("post_migrate_1_9_0", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_migration_splits_timetable_lines(self):
        """Move every old line and its attachments, and stay idempotent.

        Python-only test, trigger P10 (limitation L-11): the old rows
        are written through SQL and the migration script must be imported
        from its file, which a YAML scenario cannot do.
        """
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.7.1")
        script.migrate(self.env.cr, "14.0.1.7.1")
        self.worksheet.invalidate_cache()

        permanent = self.worksheet.permanent_ids
        current = self.worksheet.current_ids
        self.assertEqual(permanent.ids, [self.master_line_id])
        self.assertEqual(current.ids, [self.manual_line_id])
        master_line = permanent
        self.assertEqual(master_line.description, "Old master line")
        self.assertEqual(str(master_line.date), "2026-06-30")
        self.assertTrue(master_line.complete_ok)
        self.assertEqual(master_line.data_collection_id, self.master)
        self.assertEqual(master_line.data_collection_code, self.master.code)
        self.assertEqual(master_line.data_collection_code_sort, self.master.code_sort)
        self.assertEqual(master_line.category_id, self.master.category_id)
        self.assertEqual(master_line.attachment_ids, self.attachment)
        manual_line = current
        self.assertEqual(manual_line.description, "Old manual line")
        self.assertFalse(manual_line.date)
        self.assertFalse(manual_line.complete_ok)
        self.assertFalse(manual_line.data_collection_id)
        self.assertFalse(manual_line.attachment_ids)
        self.assertFalse(self.worksheet.reporting_timetable_ids)
        self.assertEqual(self.attachment.res_model, "general_audit_ws_f5a3cee")
        self.assertEqual(self.attachment.res_id, self.worksheet.id)

        values = {"worksheet_id": self.worksheet.id, "description": "After migration"}
        self.assertGreater(permanent.create(values).id, self.master_line_id)
        self.assertGreater(current.create(values).id, self.manual_line_id)

    def test_migration_keeps_lines_of_the_new_timetable(self):
        """Leave the timetable alone once the old columns are gone.

        Python-only test, trigger P10 (limitation L-11): the migration
        script must be imported from its file, which ``EVAL:`` cannot do.
        """
        self.env.cr.execute(
            """
            ALTER TABLE general_audit_ws_f5a3cee_reporting_timetable
                DROP COLUMN complete_ok
            """
        )
        self._load_script().migrate(self.env.cr, "14.0.1.7.1")
        self.worksheet.invalidate_cache()

        self.assertEqual(
            sorted(self.worksheet.reporting_timetable_ids.ids),
            [self.master_line_id, self.manual_line_id],
        )
        self.assertFalse(self.worksheet.permanent_ids)
        self.assertFalse(self.worksheet.current_ids)
