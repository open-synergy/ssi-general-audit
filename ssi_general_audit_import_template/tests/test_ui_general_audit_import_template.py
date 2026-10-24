# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase has no cls.env
# in setUpClass, and the Pre-Condition fixture below needs it there.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiGeneralAuditImportTemplate(HttpSavepointCase):
    """Tour tests for the ``general_audit_import_template`` instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the template the server action tour starts from.

        The create tour builds its own template through the UI. The
        server action tour needs a saved template without a server
        action, named ``TOUR-IMPORT-TEMPLATE``.
        """
        super().setUpClass()
        target = cls.env.ref("ssi_general_audit.model_client_business_process")
        cls.env["general_audit_import_template"].create(
            {
                "name": "TOUR-IMPORT-TEMPLATE",
                "code": "/",
                "model_id": target.id,
                "line_ids": [(0, 0, {"name": "TOUR-FIXTURE-COLUMN"})],
            }
        )

    def test_create(self):
        """Run the create tour for ``general_audit_import_template``.

        IK: docs/general_audit_import_template/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_general_audit_import_template_create",
            login="admin",
        )

    def test_create_server_action(self):
        """Run the create server action tour for the import template.

        IK: docs/general_audit_import_template/02-create-server-action.md
        """
        self.start_tour(
            "/web",
            "ssi_general_audit_import_template_create_server_action",
            login="admin",
        )
