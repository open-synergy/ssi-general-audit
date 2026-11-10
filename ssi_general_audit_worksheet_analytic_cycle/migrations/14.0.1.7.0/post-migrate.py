# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
#
# Migration: 14.0.1.6.1 -> 14.0.1.7.0
#
# Changes: ``general_audit_ws_a3c9d2e._inverse_to_standard_detail`` now
#          recomputes ``analytical_procedures_cycle_result`` from every
#          non-cancelled worksheet covering an account and clears it when
#          none remains. Earlier versions only ever wrote a value, so
#          accounts removed from a worksheet, or whose worksheet was
#          emptied, cancelled or deleted, kept a stale value that this
#          script clears. It is a "post" script because it reads
#          the relation and columns of the already-updated schema.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute the cycle result of every standard detail.

    Uses the same rule as the model: ``high`` outranks ``moderate``
    among non-cancelled worksheets of the same General Audit that tag
    the account and have a ``result``; otherwise the value is cleared.
    Only rows whose value differs are written, so it can be re-run.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``general_audit_standard_detail`` rows
    """
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE general_audit_standard_detail sd
        SET analytical_procedures_cycle_result = calc.value
        FROM (
            SELECT
                s.id,
                (
                    SELECT CASE
                        WHEN bool_or(a.result = 'high') THEN 'high'
                        WHEN count(a.id) > 0 THEN 'moderate'
                    END
                    FROM general_audit_ws_a3c9d2e a
                    JOIN general_audit_worksheet w ON w.id = a.worksheet_id
                    JOIN rel_general_audit_ws_a3c9d2e_2_account_type r
                        ON r.worksheet_id = a.id
                    WHERE w.general_audit_id = s.general_audit_id
                      AND r.type_id = s.type_id
                      AND a.state != 'cancel'
                      AND a.result IN ('high', 'moderate')
                ) AS value
            FROM general_audit_standard_detail s
        ) calc
        WHERE calc.id = sd.id
          AND sd.analytical_procedures_cycle_result IS DISTINCT FROM calc.value
        """,
    )
    _logger.info(
        "Recomputed analytical_procedures_cycle_result on %s "
        "general_audit_standard_detail row(s).",
        rows,
    )
