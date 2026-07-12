# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Trial Balance",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # MASTER DATA
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_ws_a033cc6_item.xml",
        # a033cc6
        "security/res_group/general_audit_ws_a033cc6.xml",
        "security/ir_rule/general_audit_ws_a033cc6.xml",
        "data/ir_sequence/general_audit_ws_a033cc6.xml",
        "data/sequence_template/general_audit_ws_a033cc6.xml",
        "data/policy_template/general_audit_ws_a033cc6.xml",
        "data/approval_template/general_audit_ws_a033cc6.xml",
        "views/general_audit_ws_a033cc6_views.xml",
        "views/general_audit_ws_a033cc6_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
