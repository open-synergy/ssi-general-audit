# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditConclusionMixin(models.AbstractModel):
    """Memorandum side of the per-type conclusion summary lines.

    A memorandum worksheet inherits this mixin and sets
    ``_conclusion_line_model`` and ``_conclusion_line_owner_field``.
    ``_reload_conclusion_lines`` then creates the missing lines for the
    worksheet types listed in ``conclusion_source_type_ids`` of its own
    worksheet type.
    """

    _name = "general_audit_conclusion_mixin"
    _description = "General Audit Conclusion Mixin"

    # Technical name of the concrete line model
    _conclusion_line_model = False
    # Many2one on the line model that points to the memorandum
    _conclusion_line_owner_field = False

    def _reload_conclusion_lines(self):
        """Create the missing conclusion lines and refresh all of them.

        A line is added for each source worksheet type that has at least one
        open or done worksheet in the same General Audit. Existing lines are
        never deleted and their typed summary is never changed.

        :return: ``None``.
        """
        Line = self.env[self._conclusion_line_model]
        Worksheet = self.env["general_audit_worksheet"]
        owner_field = self._conclusion_line_owner_field
        for record in self:
            lines = Line.search([(owner_field, "=", record.id)])
            missing = record.type_id.conclusion_source_type_ids - lines.mapped(
                "type_id"
            )
            for worksheet_type in missing:
                criteria = [
                    ("general_audit_id", "=", record.general_audit_id.id),
                    ("parent_type_id", "=", worksheet_type.id),
                    ("state", "in", ["open", "done"]),
                ]
                if Worksheet.search_count(criteria):
                    lines += Line.create(
                        {
                            owner_field: record.id,
                            "general_audit_id": record.general_audit_id.id,
                            "type_id": worksheet_type.id,
                        }
                    )
            lines._refresh_conclusion()
