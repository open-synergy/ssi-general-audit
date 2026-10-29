# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_open_general_audit


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsd8aaebc(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_d8aaebc`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit for the Create tour.

        The Create tour selects the audit by its fixed number
        ``TOUR-D8AAEBC-GA`` and creates its own worksheet against it, so the
        audit must not have a ``general_audit_ws_d8aaebc`` worksheet yet.
        """
        super().setUpClass()
        cls.audit = create_open_general_audit(cls.env, "TOUR-D8AAEBC-GA")

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_d8aaebc/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_engagement_letter_checklist_d8aaebc_create",
            login="admin",
        )
