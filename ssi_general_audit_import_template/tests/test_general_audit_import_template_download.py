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


@tagged("post_install", "-at_install")
class TestGeneralAuditImportTemplateDownload(YamlTransactionCase):
    """Return value tests for ``action_download`` of the import template."""

    def setUp(self):
        """Create a template with two columns on a Business Cycle model.

        The template uses ``;`` as delimiter so the tests also prove the
        delimiter is honoured.
        """
        super().setUp()
        target = self.env.ref("ssi_general_audit.model_client_business_process")
        self.template = self.env["general_audit_import_template"].create(
            {
                "name": "Test Download Template",
                "code": "/",
                "model_id": target.id,
                "file_name": "test_download.csv",
                "delimiter": ";",
                "has_header": True,
                "line_ids": [
                    (
                        0,
                        0,
                        {"sequence": 10, "name": "Second", "example_value": "b"},
                    ),
                    (
                        0,
                        0,
                        {"sequence": 5, "name": "First", "example_value": "a"},
                    ),
                ],
            }
        )

    def _read_download(self, template):
        """Return the decoded CSV text and the action of a download.

        :param template: the import template to download
        :return: tuple of the ``act_url`` dict and the CSV text
        """
        action = template.action_download()
        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", template._name),
                ("res_id", "=", template.id),
            ],
            order="id desc",
            limit=1,
        )
        return action, base64.b64decode(attachment.datas).decode("utf-8")

    def test_download_with_header(self):
        """Assert the action dict and the CSV text with a header row.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot assert the ``act_url`` dict).
        """
        action, text = self._read_download(self.template)
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn("/web/content/", action["url"])
        self.assertIn("download=true", action["url"])
        self.assertEqual(text, "First;Second\na;b\n")

    def test_download_without_header(self):
        """Assert the CSV text holds only the example row.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot assert the ``act_url`` dict).
        """
        self.template.write({"has_header": False})
        action, text = self._read_download(self.template)
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(text, "a;b\n")

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
                "ssi_general_audit_import_template",
                filename,
                {},
                mode="update",
                noupdate=False,
                kind="data",
            )
        self.env["general_audit_import_template"].invalidate_cache()
        self.env["general_audit_import_template.line"].invalidate_cache()

    def _seed(self, xml_id="general_audit_import_template_client_account_mapping"):
        """Return a seed record of the module.

        :param xml_id: the xml id without the module prefix
        :return: the seed record
        """
        return self.env.ref("ssi_general_audit_import_template." + xml_id)

    def test_seed_follows_module_update(self):
        """Assert a module update restores the seed name and columns.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        file the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self._seed()
        seed_line = self._seed(
            "general_audit_import_template_client_account_mapping_line_1"
        )
        original_name = seed.name
        original_line_name = seed_line.name
        original_count = len(seed.line_ids)
        seed.write({"name": "Renamed By Admin"})
        seed_line.write({"name": "Renamed Column"})
        other_line = self._seed(
            "general_audit_import_template_client_account_mapping_line_2"
        )
        other_line.unlink()
        self.assertEqual(len(seed.line_ids), original_count - 1)
        self._reload_data()
        self.assertEqual(seed.name, original_name)
        self.assertEqual(seed_line.name, original_line_name)
        self.assertEqual(len(seed.line_ids), original_count)
        self.assertTrue(
            self._seed(
                "general_audit_import_template_client_account_mapping_line_2"
            ).exists()
        )

    def test_seed_server_action_not_recreated(self):
        """Assert a module update does not bring the server action back.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        files the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self._seed()
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
        seed = self._seed()
        seed.write({"active": False})
        self._reload_data()
        self.assertFalse(seed.active)

    def test_pre_migrate_resets_noupdate(self):
        """Assert the pre-migrate script makes the seed updatable.

        Pure Python -- trigger P10 (L-09: the migration function is
        called directly on seed rows set back to ``noupdate``).
        """
        module = "ssi_general_audit_import_template"
        path = os.path.join(
            get_module_path(module),
            "migrations",
            "14.0.1.2.0",
            "pre-migrate.py",
        )
        spec = importlib.util.spec_from_file_location("pre_migrate_test", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        models = ("general_audit_import_template", "general_audit_import_template.line")
        self.env.cr.execute(
            "UPDATE ir_model_data SET noupdate = true "
            "WHERE module = %s AND model IN %s",
            (module, models),
        )
        script.migrate(self.env.cr, "14.0.1.1.0")
        self.env.cr.execute(
            "SELECT count(*) FROM ir_model_data "
            "WHERE module = %s AND model IN %s AND noupdate IS TRUE",
            (module, models),
        )
        self.assertEqual(self.env.cr.fetchone()[0], 0)
