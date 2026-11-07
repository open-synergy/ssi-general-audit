# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditPopulationType(HttpSavepointCase):
    """Tour tests for the ``general_audit_population_type`` instructions."""

    def test_create(self):
        """Run the Create tour.

        IK: docs/general_audit_population_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_population_type_create",
            login="admin",
        )
