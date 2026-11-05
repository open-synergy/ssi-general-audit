# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.4.15.2 -> 14.0.4.15.3
#
# Changes: only adjustment entries in done state and corrected count in the
#          account and account type adjustments. Stored figures computed
#          under the old rule (every state counted) are recomputed.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute the stored adjustment figures of every audit.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes ``general_audit.detail`` and
        ``general_audit.standard_detail`` stored fields
    """
    env["client_adjustment_entry"].flush()
    env["client_adjustment_entry.detail"].flush()
    Detail = env["general_audit.detail"]
    StandardDetail = env["general_audit.standard_detail"]
    details = Detail.search([])
    standards = StandardDetail.search([])
    # Row ids of the SQL views are not stable: relink first, so the
    # amounts below never read a row that no longer exists.
    env.add_to_compute(Detail._fields["adjustment_id"], details)
    env.add_to_compute(StandardDetail._fields["standard_adjustment_id"], standards)
    details.recompute()
    standards.recompute()
    details.flush()
    standards.flush()
    for name in ("adjustment_debit", "adjustment_credit"):
        env.add_to_compute(Detail._fields[name], details)
        env.add_to_compute(StandardDetail._fields[name], standards)
    details.recompute()
    standards.recompute()
    details.flush()
    standards.flush()
    env.add_to_compute(Detail._fields["adjustment_balance"], details)
    env.add_to_compute(Detail._fields["audited_balance"], details)
    env.add_to_compute(StandardDetail._fields["audited_balance"], standards)
    details.recompute()
    standards.recompute()
    details.flush()
    standards.flush()
    _logger.info(
        "Recomputed adjustment figures of %s detail(s) and %s standard " "detail(s).",
        len(details),
        len(standards),
    )
