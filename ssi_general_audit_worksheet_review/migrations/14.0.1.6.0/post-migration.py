# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.5.2 -> 14.0.1.6.0
#
# Changes: the opinion and the opinion date of a General Audit are no
#          longer typed in; they mirror the Independent Auditor Report
#          of the engagement (general_audit_ws_b66777d) and stay empty
#          until that report has them. Opinions typed in before this
#          version are therefore emptied, or replaced by the value of
#          the Independent Auditor Report when the engagement already
#          has one. Writing through the ORM also refreshes the stored
#          copies of these fields on other worksheets.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Align the opinion of every General Audit with its audit report.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; calls ``_sync_opinion_from_audit_report`` on
        every General Audit and logs how many carried an opinion
        before and after
    """
    audits = env["general_audit"].with_context(active_test=False).search([])
    before = len(audits.filtered(lambda a: a.opinion_id or a.opinion_date))
    audits._sync_opinion_from_audit_report()
    audits.invalidate_cache()
    after = len(audits.filtered(lambda a: a.opinion_id or a.opinion_date))
    _logger.info(
        "General Audit opinion aligned with the Independent Auditor "
        "Report: %s audits had an opinion before, %s after (of %s).",
        before,
        after,
        len(audits),
    )
