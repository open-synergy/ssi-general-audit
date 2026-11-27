# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_open_general_audit, create_populate_worksheet


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsF5a3cee(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_f5a3cee`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records of the Create and Populate Details tours.

        The Populate Details tour opens the worksheet of the General Audit
        ``TOUR-F5A3CEE-POPULATE``.  The Create tour selects the audit by its fixed number
        ``TOUR-F5A3CEE-GA`` and creates its own worksheet against it, so the
        audit must not have a ``general_audit_ws_f5a3cee`` worksheet yet.
        """
        super().setUpClass()
        cls.audit = create_open_general_audit(cls.env, "TOUR-F5A3CEE-GA")
        cls.worksheet = create_populate_worksheet(cls.env, "TOUR-F5A3CEE-POPULATE")

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_f5a3cee/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_client_package_f5a3cee_create",
            login="admin",
        )

    def test_populate_details(self):
        """Run the Populate Details tour.

        IK: docs/general_audit_ws_f5a3cee/02-populate-details.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_client_package_f5a3cee_populate_details",
            login="admin",
        )
