# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_open_general_audit


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsD4d1ac0(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_d4d1ac0`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit.

        The Create tour selects the audit by its fixed number
        ``TOUR-D4D1AC0-GA``, then creates its own worksheet.
        """
        super().setUpClass()
        cls.audit = create_open_general_audit(cls.env, "TOUR-D4D1AC0-GA")

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_d4d1ac0/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_audit_procedure_observation_d4d1ac0_create",
            login="admin",
        )
