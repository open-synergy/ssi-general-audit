# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged

from .ui_fixture import create_data_collection_refs


@tagged("post_install", "-at_install")
class TestUiGeneralAuditDataCollection(HttpSavepointCase):
    """Tour tests for the Data Collection master data instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the account type and category the Create tours pick.

        The Data Collection tour selects both by their fixed names
        ``Test Account Type - TOUR-DC`` and ``Test Category - TOUR-DC``.
        """
        super().setUpClass()
        cls.account_type, cls.category = create_data_collection_refs(cls.env, "TOUR-DC")

    def test_create_category(self):
        """Run the Create tour of the Data Collection Category.

        IK: docs/general_audit_data_collection_category/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_client_package_data_collection_category_create",
            login="admin",
        )

    def test_create(self):
        """Run the Create tour of the Data Collection.

        IK: docs/general_audit_data_collection/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_worksheet_client_package_data_collection_create",
            login="admin",
        )
