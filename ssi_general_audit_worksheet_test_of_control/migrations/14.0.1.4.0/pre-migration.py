# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Drop the old varchar toc_reference column.

    ``toc_reference`` on ``general_audit_ws_eabdaad.detail`` changes from a
    plain ``Char`` (holding the ToC worksheet's document number as text) to
    a ``Many2one`` (so it is clickable in the UI). The column type cannot be
    altered in place, so drop it here -- ``_auto_init`` recreates it as an
    integer FK and the stored related field recomputes automatically on
    module update.
    """
    _logger.info(
        "Dropping general_audit_ws_eabdaad_detail.toc_reference "
        "(varchar) before it is recreated as Many2one..."
    )
    cr.execute(
        """
        ALTER TABLE general_audit_ws_eabdaad_detail
        DROP COLUMN IF EXISTS toc_reference
        """
    )
