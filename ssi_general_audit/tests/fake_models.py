# Copyright 2026 PT. Open Source Integra Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditWorksheetTester(models.Model):
    """Minimal concrete model used only to exercise ``general_audit_worksheet_mixin``.

    The mixin is a ``models.AbstractModel`` with no concrete implementation
    inside ``ssi_general_audit`` itself (concrete worksheets live in sibling
    modules such as ``ssi_general_audit_worksheet_trial_balance``, which this
    module cannot depend on). Registered at test time only via
    ``odoo_test_helper.FakeModelLoader`` in ``test_general_audit.py``.
    """

    _name = "general_audit_worksheet_tester"
    _description = "General Audit Worksheet Tester (test-only)"
    _inherit = ["general_audit_worksheet_mixin"]
