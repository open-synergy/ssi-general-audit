# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Worksheets general_audit_ws_a13a30e / bdcdfc5 / f6a227 / c0d0898 / e78a3c6 /
# ae11f7e, the "impacted" computes on general_audit / general_audit.standard_detail
# added by this module, `_compute_standard_detail_ids` on a handful of their
# detail models, and the `onchange_partner_name` onchange on
# general_audit_ws_ae11f7e.other_evidence.

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestWorksheetImpact(YamlTransactionCase):
    def test_worksheet_impact(self):
        self.run_yaml_scenario("test_data_worksheet_impact.yaml")
