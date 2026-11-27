# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

OLD_TABLE = "general_audit_ws_f5a3cee_reporting_timetable"
OLD_RELATION = "rel_ga_f5a3cee_reporting_timetable_2_attachment"
# Current File goes last because it also takes every line that is not
# Permanent File.
TARGETS = (
    ("permanent", "m.type = 'permanent_file'"),
    ("current", "m.type IS DISTINCT FROM 'permanent_file'"),
)


@openupgrade.migrate()
def migrate(env, version):
    """Split the old reporting timetable into Permanent and Current lines.

    A line whose Data Collection master item is of type Permanent File is
    copied to ``general_audit_ws_f5a3cee.permanent``.  Every other line,
    including a line without a master item, is copied to
    ``general_audit_ws_f5a3cee.current``.  Ids and attachment links are
    kept, the attachments themselves are not changed, and the copied lines
    are removed from the reporting timetable.  The reporting timetable
    links of the Planning Memorandum are removed by the database along with
    the old lines.

    The ``complete_ok`` column only exists in the old layout of the table
    and Odoo drops it at the end of the update. Without it there is nothing
    to move, so lines entered in the new timetable are never taken.

    :param env: the migration environment
    :param str version: version being migrated to (unused)
    """
    cr = env.cr
    if not openupgrade.column_exists(cr, OLD_TABLE, "complete_ok"):
        _logger.info("No old reporting timetable data to move.")
        return
    for key, condition in TARGETS:
        line_ids = _copy_lines(cr, key, condition)
        if not line_ids:
            continue
        _copy_attachment_links(cr, key, line_ids)
        _reset_sequence(cr, key)
        openupgrade.logged_query(
            cr,
            """
            DELETE FROM general_audit_ws_f5a3cee_reporting_timetable
            WHERE id IN %s
            """,
            (line_ids,),
        )
        env["general_audit_ws_f5a3cee.%s" % key].invalidate_cache()
    env["general_audit_ws_f5a3cee.reporting_timetable"].invalidate_cache()
    env["general_audit_ws_f5a3cee"].invalidate_cache()


def _copy_lines(cr, key, condition):
    """Copy old timetable lines to one file line table, keeping their id.

    The code and sort key are read from the master item, so they are right
    even when the stored copy of the old line was never rebuilt.

    :param cr: the database cursor
    :param str key: suffix of the target table
    :param str condition: SQL condition on the master item of the lines
    :return: ids of the copied lines
    :rtype: tuple
    """
    table = "general_audit_ws_f5a3cee_%s" % key
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO {table} (
            id, worksheet_id, data_collection_id, data_collection_code,
            data_collection_code_sort, category_id, description, date,
            complete_ok, create_uid, create_date, write_uid, write_date
        )
        SELECT
            t.id, t.worksheet_id, t.data_collection_id, m.code,
            m.code_sort, t.category_id, t.description, t.date,
            t.complete_ok, t.create_uid, t.create_date, t.write_uid,
            t.write_date
        FROM general_audit_ws_f5a3cee_reporting_timetable AS t
        LEFT JOIN general_audit_data_collection AS m
            ON m.id = t.data_collection_id
        WHERE {condition}
        AND NOT EXISTS (
            SELECT 1 FROM {table} AS o
            WHERE o.id = t.id
        )
        RETURNING id
        """.format(
            table=table, condition=condition
        ),
    )
    return tuple(row[0] for row in cr.fetchall())


def _copy_attachment_links(cr, key, line_ids):
    """Copy the attachment links of the copied lines.

    :param cr: the database cursor
    :param str key: suffix of the target table
    :param tuple line_ids: ids of the copied lines
    """
    if not openupgrade.table_exists(cr, OLD_RELATION):
        return
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO rel_ga_f5a3cee_{key}_2_attachment
            (f5a3cee_{key}_id, attachment_id)
        SELECT f5a3cee_reporting_timetable_id, attachment_id
        FROM rel_ga_f5a3cee_reporting_timetable_2_attachment
        WHERE f5a3cee_reporting_timetable_id IN %s
        """.format(
            key=key
        ),
        (line_ids,),
    )


def _reset_sequence(cr, key):
    """Move the id sequence of a file line table past the copied ids.

    :param cr: the database cursor
    :param str key: suffix of the table
    """
    table = "general_audit_ws_f5a3cee_%s" % key
    openupgrade.logged_query(
        cr,
        """
        SELECT setval(
            pg_get_serial_sequence('{table}', 'id'),
            (SELECT MAX(id) FROM {table})
        )
        """.format(
            table=table
        ),
    )
