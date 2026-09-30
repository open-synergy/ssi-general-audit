# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.4.0 -> 14.0.1.5.0
#
# Changes: the names of the worksheet types, window actions and menus
#          of general_audit_ws_be62e79 and general_audit_ws_a025441 are
#          swapped ("Financial Statement Disclosure" and "Financial
#          Statement Disclosure - Detail"). Odoo keeps an existing
#          translation value when the source term changes, so the
#          Indonesian names would stay attached to the old English
#          names. This script rewrites the id_ID translation of these
#          six records to match the new names.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_MODULE = "ssi_general_audit_worksheet_review"

_NAMES = (
    (
        "be62e79",
        "Financial Statement Disclosure",
        "Pengungkapan Laporan Keuangan",
    ),
    (
        "a025441",
        "Financial Statement Disclosure - Detail",
        "Pengungkapan Laporan Keuangan - Detail",
    ),
)

_RECORDS = (
    ("general_audit_worksheet_type,name", "worksheet_type_%s"),
    ("ir.actions.act_window,name", "general_audit_ws_%s_action"),
    ("ir.ui.menu,name", "general_audit_ws_%s_menu"),
)


@openupgrade.migrate()
def migrate(env, version):
    """Rewrite the id_ID translation of the swapped names.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``ir_translation`` rows
    """
    for code, source, value in _NAMES:
        for field_name, xml_id_pattern in _RECORDS:
            record = env.ref(
                "%s.%s" % (_MODULE, xml_id_pattern % code),
                raise_if_not_found=False,
            )
            if not record:
                continue
            rows = openupgrade.logged_query(
                env.cr,
                """
                UPDATE ir_translation
                SET src = %s, value = %s, state = 'translated'
                WHERE lang = 'id_ID'
                    AND type = 'model'
                    AND name = %s
                    AND res_id = %s
                """,
                (source, value, field_name, record.id),
            )
            _logger.info("Updated %s translation row(s) of %s.", rows, field_name)
