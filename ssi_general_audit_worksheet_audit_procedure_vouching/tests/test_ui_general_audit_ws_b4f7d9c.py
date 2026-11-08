# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_open_general_audit


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsB4f7d9c(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_b4f7d9c`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit.

        The Create tour selects the audit by its fixed number
        ``TOUR-B4F7D9C-GA``, then creates its own worksheet.
        """
        super().setUpClass()
        cls.audit = create_open_general_audit(cls.env, "TOUR-B4F7D9C-GA")

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_b4f7d9c/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_audit_procedure_vouching_b4f7d9c_create",
            login="admin",
        )
