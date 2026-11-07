# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_open_general_audit, create_population_type


@tagged("post_install", "-at_install")
class TestUiGeneralAuditWsA01723b(HttpSavepointCase):
    """Tour tests for the ``general_audit_ws_a01723b`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create an open General Audit and a Population Type.

        The Create tour selects the audit by its fixed number
        ``TOUR-A01723B-GA`` and the type by its name ``TOUR-POP-TYPE``,
        then creates its own worksheet.
        """
        super().setUpClass()
        cls.audit = create_open_general_audit(cls.env, "TOUR-A01723B-GA")
        cls.population_type = create_population_type(cls.env, "TOUR-POP-TYPE")

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_ws_a01723b/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_population_a01723b_create",
            login="admin",
        )
