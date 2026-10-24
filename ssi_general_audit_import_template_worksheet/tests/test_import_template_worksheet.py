# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64
import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged
from odoo.tools import convert_file

MODULE = "ssi_general_audit_import_template_worksheet"

COLUMNS = {
    "financial_statement_disclosure": ["Item", "Standard", "Note", "Status"],
    "population": ["ID", "Date", "Reference", "Amount"],
    "subledger": ["No", "Name", "Reference", "Date", "Due Date", "Amount"],
    "general_ledger": [
        "Date",
        "Reference",
        "Account Code",
        "Account Name",
        "Description",
        "Debit",
        "Credit",
    ],
}


@tagged("post_install", "-at_install")
class TestImportTemplateWorksheet(YamlTransactionCase):
    """Tests for the seeded worksheet import templates."""

    def test_seed_scenarios(self):
        """Run the seed scenarios: model, column count, server action."""
        self.run_yaml_scenario("test_data_import_template_worksheet.yaml")

    def _get_template(self, key):
        """Return the seeded template of a key.

        :param key: suffix of the template xml id
        :return: the ``general_audit_import_template`` record
        """
        return self.env.ref(
            "ssi_general_audit_import_template_worksheet."
            "general_audit_import_template_" + key
        )

    def test_column_order(self):
        """Assert the columns of each seed in written order.

        Pure Python -- trigger P3 (L-06: o2m rows are compared as a set,
        so YAML cannot assert their order).
        """
        for key, expected in COLUMNS.items():
            template = self._get_template(key)
            lines = template.line_ids.sorted(lambda r: (r.sequence, r.id))
            self.assertEqual(lines.mapped("name"), expected, key)

    def test_download_review_template(self):
        """Assert the review seed downloads a CSV with its header row.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot read the generated attachment).
        """
        template = self._get_template("financial_statement_disclosure")
        template.action_download()
        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", template._name),
                ("res_id", "=", template.id),
            ],
            order="id desc",
            limit=1,
        )
        text = base64.b64decode(attachment.datas).decode("utf-8")
        self.assertEqual(
            text.splitlines()[0],
            "Item,Standard,Note,Status",
        )

    def _reload_data(self, with_server_action=False):
        """Reload the data files the way ``-u`` does.

        :param with_server_action: also reload the noupdate file that
            holds the call creating the server actions
        :return: nothing; the data files are loaded in update mode
        """
        files = ["data/general_audit_import_template_data.xml"]
        if with_server_action:
            files.append("data/general_audit_import_template_server_action.xml")
        for filename in files:
            convert_file(
                self.env.cr,
                MODULE,
                filename,
                {},
                mode="update",
                noupdate=False,
                kind="data",
            )
        self.env["general_audit_import_template"].invalidate_cache()
        self.env["general_audit_import_template.line"].invalidate_cache()

    def test_seed_follows_module_update(self):
        """Assert a module update restores the seed name and columns.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        file the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self._get_template("general_ledger")
        seed_line = self.env.ref(
            MODULE + ".general_audit_import_template_general_ledger_line_1"
        )
        other_line = self.env.ref(
            MODULE + ".general_audit_import_template_general_ledger_line_2"
        )
        original_name = seed.name
        original_line_name = seed_line.name
        original_count = len(seed.line_ids)
        seed.write({"name": "Renamed By Admin"})
        seed_line.write({"name": "Renamed Column"})
        other_line.unlink()
        self.assertEqual(len(seed.line_ids), original_count - 1)
        self._reload_data()
        self.assertEqual(seed.name, original_name)
        self.assertEqual(seed_line.name, original_line_name)
        self.assertEqual(len(seed.line_ids), original_count)
        # unlink() drops the xmlid, so the reload recreates a new record.
        self.assertFalse(other_line.exists())
        restored = self.env.ref(
            MODULE + ".general_audit_import_template_general_ledger_line_2"
        )
        self.assertIn(restored, seed.line_ids)

    def test_seed_server_action_not_recreated(self):
        """Assert a module update does not bring the server action back.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        files the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self._get_template("population")
        self.assertTrue(seed.server_action_id)
        seed.action_remove_server_action()
        self.assertFalse(seed.server_action_id)
        self._reload_data(with_server_action=True)
        self.assertFalse(seed.server_action_id)

    def test_seed_archived_stays_archived(self):
        """Assert a module update keeps an archived seed archived.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        file the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self._get_template("subledger")
        seed.write({"active": False})
        self._reload_data()
        self.assertFalse(seed.active)

    def test_pre_migrate_resets_noupdate(self):
        """Assert the pre-migrate script makes the seed updatable.

        Pure Python -- trigger P10 (L-09: the migration function is
        called directly on seed rows set back to ``noupdate``).
        """
        path = os.path.join(
            get_module_path(MODULE),
            "migrations",
            "14.0.1.1.0",
            "pre-migrate.py",
        )
        spec = importlib.util.spec_from_file_location("pre_migrate_test", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        models = ("general_audit_import_template", "general_audit_import_template.line")
        self.env.cr.execute(
            "UPDATE ir_model_data SET noupdate = true "
            "WHERE module = %s AND model IN %s",
            (MODULE, models),
        )
        script.migrate(self.env.cr, "14.0.1.0.2")
        self.env.cr.execute(
            "SELECT count(*) FROM ir_model_data "
            "WHERE module = %s AND model IN %s AND noupdate IS TRUE",
            (MODULE, models),
        )
        self.assertEqual(self.env.cr.fetchone()[0], 0)
