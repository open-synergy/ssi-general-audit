# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGeneralAudit(YamlTransactionCase):
    def test_general_audit(self):
        self.run_yaml_scenario("test_data_general_audit.yaml")

    def test_default_service_id_not_found(self):
        """Assert ``_default_service_id`` returns ``False`` when unset.

        Pure Python -- trigger P1 (L-01: the method's return value is
        not a record field, so no YAML action can capture it).
        Relies on Odoo test isolation (this test method's transaction
        starts from the clean post-install baseline, not from
        mutations made by other test methods): ``accountant.service``
        ships no official master data in this module -- only demo
        records under different names -- so "Historical Audit
        Services" does not exist yet at the start of this method,
        exactly the condition ``_default_service_id`` must handle
        without raising (issue #361).
        """
        self.assertFalse(self.env["general_audit"]._default_service_id())

    def test_default_service_id_found(self):
        """Assert ``_default_service_id`` finds the service by name.

        Pure Python -- trigger P1 (L-01; full rationale under
        ``test_default_service_id_not_found``). Looked up by
        ``name``, not ``env.ref()`` -- full rationale in
        ``general_audit._default_service_id``'s own docstring.
        """
        service = self.env["accountant.service"].create(
            {"name": "Historical Audit Services", "code": "/"}
        )
        self.assertEqual(self.env["general_audit"]._default_service_id(), service.id)
