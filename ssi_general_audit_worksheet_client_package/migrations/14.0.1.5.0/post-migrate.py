# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Move date, attachments and completion of old details to data lines.

    Every Data Collection detail (f5a3cee) that had a date, attachments or
    was completed gets one data line without master item holding the same
    values.  The old columns are left in place; the fields no longer exist.

    :param env: the migration environment
    :param str version: version being migrated to (unused)
    """
    cr = env.cr
    cr.execute(
        """
        SELECT d.id, d.date, d.complete_ok, d.create_uid
        FROM general_audit_ws_f5a3cee_detail d
        WHERE (
            d.date IS NOT NULL OR d.complete_ok
            OR EXISTS (
                SELECT 1 FROM rel_ga_f5a3cee_detail_2_attachment r
                WHERE r.f5a3cee_detail_id = d.id
            )
        )
        AND NOT EXISTS (
            SELECT 1 FROM general_audit_ws_f5a3cee_detail_line l
            WHERE l.detail_id = d.id AND l.data_collection_id IS NULL
        )
        """
    )
    for detail_id, date, complete_ok, create_uid in cr.fetchall():
        openupgrade.logged_query(
            cr,
            """
            INSERT INTO general_audit_ws_f5a3cee_detail_line
                (detail_id, name, date, complete_ok, create_uid, write_uid,
                 create_date, write_date)
            VALUES (%s, %s, %s, %s, %s, %s, now(), now())
            RETURNING id
            """,
            (
                detail_id,
                "Migrated data",
                date,
                bool(complete_ok),
                create_uid,
                create_uid,
            ),
        )
        line_id = cr.fetchone()[0]
        openupgrade.logged_query(
            cr,
            """
            INSERT INTO rel_ga_f5a3cee_detail_line_2_attachment
                (f5a3cee_detail_line_id, attachment_id)
            SELECT %s, attachment_id
            FROM rel_ga_f5a3cee_detail_2_attachment
            WHERE f5a3cee_detail_id = %s
            """,
            (line_id, detail_id),
        )
    _logger.info("Moved data of old f5a3cee details to data lines.")
