# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.4.6.1 -> 14.0.4.6.2
#
# Changes: ``client_adjustment_entry.detail.detail_id`` is a stored compute
#          that was never recomputed when ``general_audit.detail`` records
#          were created after the adjustment lines (for example by an
#          account reload). Existing unlinked lines stay empty and are
#          excluded from ``adjustment_dr``/``adjustment_cr``.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute ``detail_id`` on adjustment lines that are still unlinked.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes ``client_adjustment_entry.detail`` rows
    """
    AdjustmentLine = env["client_adjustment_entry.detail"]
    lines = AdjustmentLine.search(
        [
            ("detail_id", "=", False),
            ("entry_id.general_audit_id", "!=", False),
        ]
    )
    env.add_to_compute(AdjustmentLine._fields["detail_id"], lines)
    lines.flush(["detail_id"])
    linked = len(lines.filtered("detail_id"))
    _logger.info(
        "Recomputed detail_id on %s adjustment line(s); %s now linked.",
        len(lines),
        linked,
    )
