# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.13.0 -> 14.0.1.14.0
#
# Changes: the Conclusions tab now shows one general_audit_ws_a8c54f3
#          .conclusion line per worksheet type. The free text typed in
#          the old link_N_conclusion fields is moved to the line of the
#          worksheet type behind link_N, so no typed text is lost.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Move the typed ``link_N_conclusion`` text to conclusion lines.

    For each worksheet and each Many2many link whose conclusion text is
    filled, creates the conclusion line of the linked worksheet type and
    stores the text in it. A line that already exists is left untouched.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; creates ``general_audit_ws_a8c54f3.conclusion`` lines
    """
    Worksheet = env["general_audit_ws_a8c54f3"]
    Line = env["general_audit_ws_a8c54f3.conclusion"]
    Type = env["general_audit_worksheet_type"]
    moved = 0
    for name in list(Worksheet._fields):
        if not (name.startswith("link_") and name.endswith("_conclusion")):
            continue
        link_field = Worksheet._fields.get(name[: -len("_conclusion")] + "_ids")
        if link_field is None or link_field.type != "many2many":
            continue
        worksheet_type = Type.search(
            [("model_name", "=", link_field.comodel_name)], limit=1
        )
        if not worksheet_type:
            continue
        for record in Worksheet.search([(name, "!=", False)]):
            if Line.search_count(
                [
                    ("worksheet_id", "=", record.id),
                    ("type_id", "=", worksheet_type.id),
                ]
            ):
                continue
            Line.create(
                {
                    "worksheet_id": record.id,
                    "general_audit_id": record.general_audit_id.id,
                    "type_id": worksheet_type.id,
                    "conclusion": record[name],
                }
            )
            moved += 1
    _logger.info("Moved %s link conclusion texts to lines", moved)
