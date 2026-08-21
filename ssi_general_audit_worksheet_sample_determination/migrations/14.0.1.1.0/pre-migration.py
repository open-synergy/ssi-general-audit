# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Clean up b7df2d5 worksheet data before _process_end runs."""
    _logger.info("Cleaning up b7df2d5 worksheet type references...")

    # Find b7df2d5 worksheet type IDs from ir_model_data
    cr.execute(
        """
        SELECT res_id FROM ir_model_data
        WHERE module = 'ssi_general_audit_worksheet_test_of_detail'
          AND model = 'general_audit.worksheet.type'
          AND name LIKE '%%b7df2d5%%'
        """
    )
    type_ids = [r[0] for r in cr.fetchall()]
    _logger.info("Found b7df2d5 worksheet type IDs: %s", type_ids)

    if type_ids:
        # Remove general_audit_worksheet records referencing b7df2d5 type
        cr.execute(
            """
            DELETE FROM general_audit_worksheet
            WHERE parent_type_id IN %s
            """,
            (tuple(type_ids),),
        )
        _logger.info("Deleted %d general_audit_worksheet records", cr.rowcount)

        # Remove b7df2d5 worksheet type records
        cr.execute(
            """
            DELETE FROM general_audit_worksheet_type
            WHERE id IN %s
            """,
            (tuple(type_ids),),
        )
        _logger.info("Deleted %d general_audit_worksheet_type records", cr.rowcount)

    # Remove all ir.model.data entries for b7df2d5
    cr.execute(
        """
        DELETE FROM ir_model_data
        WHERE module = 'ssi_general_audit_worksheet_test_of_detail'
          AND name LIKE '%%b7df2d5%%'
        """
    )
    _logger.info("Deleted %d ir.model.data entries for b7df2d5", cr.rowcount)
