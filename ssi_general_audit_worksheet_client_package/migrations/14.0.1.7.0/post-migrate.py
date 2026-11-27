# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

LINE_MODELS = (
    "general_audit_ws_f5a3cee.permanent",
    "general_audit_ws_f5a3cee.current",
    "general_audit_ws_f5a3cee.detail_line",
)


@openupgrade.migrate()
def migrate(env, version):
    """Rebuild the sort key of Data Collection items and their lines.

    The sort key of an item now starts with the rank of its type, so the
    stored key of every item, and the copy of it kept on the lines of the
    Data Collection worksheet, must be computed again. The recompute goes
    through ``add_to_compute`` and ``flush``, never through the compute
    method itself, so no ``write`` override runs during the update.
    The ``permanent`` and ``current`` lines are still empty when upgrading
    from this far back; migration 14.0.1.9.0 fills them with the sort key of
    their master item.

    :param env: the migration environment
    :param str version: version being migrated to (unused)
    """
    items = env["general_audit_data_collection"].with_context(active_test=False)
    items = items.search([])
    env.add_to_compute(items._fields["code_sort"], items)
    items.flush(["code_sort"])
    _logger.info("Recomputed code_sort on %s item(s).", len(items))
    for model_name in LINE_MODELS:
        lines = env[model_name].search([("data_collection_id", "!=", False)])
        field = lines._fields["data_collection_code_sort"]
        env.add_to_compute(field, lines)
        lines.flush(["data_collection_code_sort"])
        _logger.info("Recomputed sort key on %s line(s) of %s.", len(lines), model_name)
