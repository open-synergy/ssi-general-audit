# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.2.7.0 -> 14.0.2.8.0
#
# Changes: `general_audit_it_control` master data was restructured so
# that Category -> Control -> Indicator is a real 3-level hierarchy
# (issue #299): 18 new `general_audit_it_control` records were added
# and `general_audit_it_control_indicator.control_id` was re-pointed
# from a single per-category placeholder control to the correct
# control. By the time this post-script runs, the master data XML has
# already been reloaded, so `indicator_id.control_id` on every
# checklist line already carries the corrected value. What has NOT
# been touched yet is existing `general_audit_ws_f63f569.detail` /
# `.indicator` rows (worksheet transaction data): every indicator line
# created before this fix still hangs off the old per-category
# placeholder detail row, because Odoo only reloads master data -- it
# never re-derives transaction rows that were built from it. This
# script moves each indicator line onto the detail row matching its
# now-correct control, creating that detail row if it does not exist
# yet, so existing worksheets end up with the same structure a fresh
# `action_load_detail()` would produce -- without discarding any
# `result`/`explanation` already recorded at the indicator level.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Re-point IT Control Evaluation indicator lines to the right detail.

    Uses the ORM instead of raw SQL: `general_audit_ws_f63f569.detail`
    carries a stored related field (``category_id``) that must stay
    consistent with the target control, and the affected data is
    worksheet transaction rows (small per database), not a bulk table
    that would make row-by-row ORM writes prohibitively slow.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; creates/updates ``general_audit_ws_f63f569.detail``
        and ``general_audit_ws_f63f569.indicator`` records in place
    """
    indicator_model = env["general_audit_ws_f63f569.indicator"]
    detail_model = env["general_audit_ws_f63f569.detail"]

    moved = 0
    created_details = 0
    for line in indicator_model.search([]):
        correct_control = line.indicator_id.control_id
        current_detail = line.detail_id
        if not correct_control or correct_control == current_detail.control_id:
            continue
        target_detail = detail_model.search(
            [
                ("worksheet_id", "=", current_detail.worksheet_id.id),
                ("control_id", "=", correct_control.id),
            ],
            limit=1,
        )
        if not target_detail:
            target_detail = detail_model.create(
                {
                    "worksheet_id": current_detail.worksheet_id.id,
                    "control_id": correct_control.id,
                }
            )
            created_details += 1
        line.write({"detail_id": target_detail.id})
        moved += 1

    _logger.info(
        "IT Control Evaluation restructuring (issue #299): moved %s "
        "indicator line(s) into %s newly created detail line(s).",
        moved,
        created_details,
    )
