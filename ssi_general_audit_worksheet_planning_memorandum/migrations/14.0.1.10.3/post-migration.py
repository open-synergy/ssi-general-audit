# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.10.2 -> 14.0.1.10.3
#
# Changes: the data an Audit Planning Memorandum copies from its source
#          worksheets now follows them while the memorandum is draft or
#          open. Memorandums saved before this change hold stale copies,
#          so the links and the copied data are recomputed once.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODEL = "general_audit_ws_fbbe0f8"

COPIED_FIELDS = [
    "it_detail_ids",
    "it_review",
    "industry_review",
    "amendment_review",
    "regulatory_review",
    "unannounced_audit_ids",
    "assigned_team_member_ids",
    "volume_transaction_ids",
    "overall_materiality",
    "performance_materiality",
    "tolerable_misstatement",
    "specific_materiality_ids",
    "previous_auditor_ids",
    "other_provided_service_ids",
    "previous_audit_evidence_ids",
    "other_evidence_ids",
    "assignment_team_ids",
    "cycle_level_ids",
    "significant_acc_ids",
    "reporting_timetable_ids",
]


@openupgrade.migrate()
def migrate(env, version):
    """Recompute links and copied data of draft and open memorandums.

    Marks every stored ``link_*`` field and every field in
    ``COPIED_FIELDS`` of the memorandums that follow their sources
    (see ``_get_following_states``) for recomputation. Memorandums in
    any other state are snapshots and are left untouched.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; the recomputed values are flushed to the database
    """
    Worksheet = env[MODEL].with_context(active_test=False)
    records = Worksheet.search([("state", "in", Worksheet._get_following_states())])
    link_fields = [
        name
        for name, field in Worksheet._fields.items()
        if name.startswith("link_") and field.compute and field.store
    ]
    names = link_fields + COPIED_FIELDS
    for name in names:
        env.add_to_compute(Worksheet._fields[name], records)
    Worksheet.flush(names)
    _logger.info(
        "%s: recomputed %d links and copied fields on %d memorandums",
        MODEL,
        len(names),
        len(records),
    )
