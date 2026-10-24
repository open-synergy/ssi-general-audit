# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo_yaml_test import YamlTransactionCase

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

    def test_seed_survives_module_update(self):
        """Assert a module update keeps the admin changes on the seed.

        The seed also keeps no server action once an admin removed it.

        Pure Python -- trigger P10 (L-09: the fixture reloads the data
        file the way ``-u`` does, which a single YAML expression
        cannot).
        """
        seed = self.env.ref(
            "ssi_general_audit_import_template."
            "general_audit_import_template_client_account_mapping"
        )
        seed_line = self.env.ref(
            "ssi_general_audit_import_template."
            "general_audit_import_template_client_account_mapping_line_1"
        )
        self.assertTrue(seed.server_action_id)
        seed.action_remove_server_action()
        seed.write({"name": "Renamed By Admin"})
        seed_line.write({"name": "Renamed Column"})
        seed.write({"line_ids": [(0, 0, {"name": "Admin Column"})]})
        line_count = len(seed.line_ids)
        convert_file(
            self.env.cr,
            "ssi_general_audit_import_template",
            "data/general_audit_import_template_data.xml",
            {},
            mode="update",
            noupdate=False,
            kind="data",
        )
        seed.invalidate_cache()
        seed_line.invalidate_cache()
        self.assertEqual(seed.name, "Renamed By Admin")
        self.assertFalse(seed.server_action_id)
        self.assertEqual(seed_line.name, "Renamed Column")
        self.assertEqual(len(seed.line_ids), line_count)
