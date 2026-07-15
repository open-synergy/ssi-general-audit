# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Team Communication",
    "version": "14.0.1.1.0",
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
        "data/master/general_audit_ws_437fc8f_item.xml",
        "data/master/general_audit_ws_b1f820c_item.xml",
        # 437fc8f - Team Communication Pre-Engagement
        "security/res_group/general_audit_ws_437fc8f.xml",
        "security/ir_rule/general_audit_ws_437fc8f.xml",
        "data/ir_sequence/general_audit_ws_437fc8f.xml",
        "data/sequence_template/general_audit_ws_437fc8f.xml",
        "data/policy_template/general_audit_ws_437fc8f.xml",
        "data/approval_template/general_audit_ws_437fc8f.xml",
        "views/ga_437fc8f/general_audit_ws_437fc8f_views.xml",
        "views/ga_437fc8f/general_audit_ws_437fc8f_item_views.xml",
        # b1f820c - Team Communication Risk Assessment
        "security/res_group/general_audit_ws_b1f820c.xml",
        "security/ir_rule/general_audit_ws_b1f820c.xml",
        "data/ir_sequence/general_audit_ws_b1f820c.xml",
        "data/sequence_template/general_audit_ws_b1f820c.xml",
        "data/policy_template/general_audit_ws_b1f820c.xml",
        "data/approval_template/general_audit_ws_b1f820c.xml",
        "views/ga_b1f820c/general_audit_ws_b1f820c_views.xml",
        "views/ga_b1f820c/general_audit_ws_b1f820c_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
