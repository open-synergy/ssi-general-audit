# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.0 -> 14.0.1.1.0
#
# Changes: Performance Materiality is now read from the Final Materiality
#          worksheet instead of the Specific Materiality worksheet. The
#          stored values of existing worksheets keep the old source until
#          they are recomputed.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Recompute Performance Materiality of the existing worksheets.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes ``performance_materiality``
    """
    worksheets = env["general_audit_ws_c3b9e71"].search([])
    field = worksheets._fields["performance_materiality"]
    env.add_to_compute(field, worksheets)
    worksheets.flush(["performance_materiality"])
    _logger.info(
        "Recomputed performance_materiality on %s worksheet(s).", len(worksheets)
    )
