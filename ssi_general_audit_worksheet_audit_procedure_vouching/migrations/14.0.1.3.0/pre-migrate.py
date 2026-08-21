# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Rename test_of_detail_id to sample_determination_id.

    The field pointed at general_audit_ws_a916660, which was mislabeled
    "Test of Detail" but is actually the Sample Determination worksheet
    (see the sibling rename of ssi_general_audit_worksheet_test_of_detail
    <-> ssi_general_audit_worksheet_sample_determination). Renaming the
    column in place preserves existing data instead of dropping and
    recreating it.
    """
    cr.execute(
        """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'general_audit_ws_b4f7d9c'
          AND column_name = 'test_of_detail_id'
        """
    )
    if not cr.fetchone():
        _logger.info("test_of_detail_id column not found, nothing to rename.")
        return

    cr.execute(
        """
        ALTER TABLE general_audit_ws_b4f7d9c
        RENAME COLUMN test_of_detail_id TO sample_determination_id
        """
    )
    _logger.info(
        "Renamed general_audit_ws_b4f7d9c.test_of_detail_id "
        "to sample_determination_id."
    )
