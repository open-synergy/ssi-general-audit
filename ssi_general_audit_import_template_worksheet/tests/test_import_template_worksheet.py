# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

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
        """Run the seed scenarios: model, column count, no server action."""
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
