# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.10.5 -> 14.0.1.10.6
#
# Changes: six text fields of the Audit Planning Memorandum now take the
#          conclusion of their source worksheet instead of its review
#          notes. Memorandums saved before this change hold the review
#          notes, so the fields are recomputed once for the memorandums
#          that follow their sources.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODEL = "general_audit_ws_fbbe0f8"

CONCLUSION_FIELDS = [
    "team_pe_review",
    "control_entity_review",
    "it_review",
    "industry_review",
    "amendment_review",
    "regulatory_review",
]


@openupgrade.migrate()
def migrate(env, version):
    """Recompute the conclusion fields of draft and open memorandums.

    Marks every field in ``CONCLUSION_FIELDS`` of the memorandums that
    follow their sources (see ``_get_following_states``) for
    recomputation. Memorandums in any other state are snapshots and are
    left untouched.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; the recomputed values are flushed to the database
    """
    Worksheet = env[MODEL].with_context(active_test=False)
    records = Worksheet.search([("state", "in", Worksheet._get_following_states())])
    for name in CONCLUSION_FIELDS:
        env.add_to_compute(Worksheet._fields[name], records)
    Worksheet.flush(CONCLUSION_FIELDS)
    _logger.info(
        "%s: recomputed %d conclusion fields on %d memorandums",
        MODEL,
        len(CONCLUSION_FIELDS),
        len(records),
    )
