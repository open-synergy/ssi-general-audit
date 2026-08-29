# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
#
# Migration: 14.0.1.3.0 -> 14.0.1.4.0
#
# Changes: ``general_audit_ws_a3c9d2e`` gets its own ``result``
#          (High/Moderate) field, now the single source propagated to
#          ``standard_detail_ids.analytical_procedures_cycle_result``.
#          Previously that value was derived from ``conclusion_id``
#          matching the master High/Moderate records seeded by this
#          module (XML ID ``general_audit_worksheet_conclusion_a3c9d2e_
#          high``/``_moderate``). This is a "post" script because
#          ``result`` is a brand new column that only exists once the
#          new schema has been created.
#
# Note: ``conclusion_id`` is NOT a physical column on
#       ``general_audit_ws_a3c9d2e`` -- the mixin ``general_audit_
#       worksheet_mixin`` uses ``_inherits = {"general_audit_worksheet":
#       "worksheet_id"}``, so ``conclusion_id`` actually lives on the
#       delegated ``general_audit_worksheet`` table and is only reachable
#       here through a JOIN on ``worksheet_id``. ``result`` itself is a
#       genuine own column (not delegated).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_XMLID_MODULE = "ssi_general_audit_worksheet_analytic_cycle"
_RESULT_BY_XMLID = {
    "high": "%s.general_audit_worksheet_conclusion_a3c9d2e_high" % _XMLID_MODULE,
    "moderate": (
        "%s.general_audit_worksheet_conclusion_a3c9d2e_moderate" % _XMLID_MODULE
    ),
}


@openupgrade.migrate()
def migrate(env, version):
    """Backfill ``result`` from the legacy ``conclusion_id`` mapping.

    Existing ``general_audit_ws_a3c9d2e`` rows whose ``conclusion_id``
    pointed to this module's master High/Moderate conclusion records
    get the matching ``result`` value; every other row is left
    untouched (``result`` stays ``NULL``). This only stamps the new
    column -- it deliberately does not re-run
    ``_inverse_to_standard_detail()``, so
    ``standard_detail_ids.analytical_procedures_cycle_result`` on
    existing data is left as-is.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``general_audit_ws_a3c9d2e`` rows
    """
    cr = env.cr
    for result_value, xmlid in _RESULT_BY_XMLID.items():
        conclusion = env.ref(xmlid, raise_if_not_found=False)
        if not conclusion:
            _logger.warning(
                "XML ID %s not found; skipping result=%s backfill.",
                xmlid,
                result_value,
            )
            continue
        rows = openupgrade.logged_query(
            cr,
            """
            UPDATE general_audit_ws_a3c9d2e a
            SET result = %s
            FROM general_audit_worksheet w
            WHERE a.worksheet_id = w.id
              AND w.conclusion_id = %s
              AND a.result IS NULL
            """,
            (result_value, conclusion.id),
        )
        _logger.info(
            "Backfilled result=%s on %s general_audit_ws_a3c9d2e row(s) "
            "(conclusion_id=%s).",
            result_value,
            rows,
            conclusion.id,
        )
