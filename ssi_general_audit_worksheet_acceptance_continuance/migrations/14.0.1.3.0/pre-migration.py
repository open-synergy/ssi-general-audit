# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
import logging


def migrate(cr, version):
    """Clear stale ``fax`` data before the field is removed from the model.

    :param cr: Database cursor.
    :param version: Previously installed module version, falsy on fresh install.
    """
    if not version:
        return
    logger = logging.getLogger(__name__)
    logger.info("Clearing general_audit_ws_805d4d5.fax before field removal...")
    cr.execute("UPDATE general_audit_ws_805d4d5 SET fax = NULL;")
    logger.info("Successfully cleared general_audit_ws_805d4d5.fax")
