# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - External Communication",
    "version": "14.0.1.0.0",
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
        "data/master/general_audit_ws_ae48e68_item.xml",
        "data/master/general_audit_ws_b3ff42f_item.xml",
        "data/master/general_audit_ws_c94e287_item.xml",
        "data/master/general_audit_ws_d133f46_item.xml",
        # ae48e68 - External Communication
        "security/res_group/general_audit_ws_ae48e68.xml",
        "security/ir_rule/general_audit_ws_ae48e68.xml",
        "data/ir_sequence/general_audit_ws_ae48e68.xml",
        "data/sequence_template/general_audit_ws_ae48e68.xml",
        "data/policy_template/general_audit_ws_ae48e68.xml",
        "data/approval_template/general_audit_ws_ae48e68.xml",
        "views/ga_ae48e68/general_audit_ws_ae48e68_views.xml",
        "views/ga_ae48e68/general_audit_ws_ae48e68_item_views.xml",
        # b3ff42f - Communication With Management
        "security/res_group/general_audit_ws_b3ff42f.xml",
        "security/ir_rule/general_audit_ws_b3ff42f.xml",
        "data/ir_sequence/general_audit_ws_b3ff42f.xml",
        "data/sequence_template/general_audit_ws_b3ff42f.xml",
        "data/policy_template/general_audit_ws_b3ff42f.xml",
        "data/approval_template/general_audit_ws_b3ff42f.xml",
        "views/ga_b3ff42f/general_audit_ws_b3ff42f_views.xml",
        "views/ga_b3ff42f/general_audit_ws_b3ff42f_item_views.xml",
        # c94e287 - Communication With TCWG
        "security/res_group/general_audit_ws_c94e287.xml",
        "security/ir_rule/general_audit_ws_c94e287.xml",
        "data/ir_sequence/general_audit_ws_c94e287.xml",
        "data/sequence_template/general_audit_ws_c94e287.xml",
        "data/policy_template/general_audit_ws_c94e287.xml",
        "data/approval_template/general_audit_ws_c94e287.xml",
        "views/ga_c94e287/general_audit_ws_c94e287_views.xml",
        "views/ga_c94e287/general_audit_ws_c94e287_item_views.xml",
        # d133f46 - Use of Internal Auditor's Work Results
        "security/res_group/general_audit_ws_d133f46.xml",
        "security/ir_rule/general_audit_ws_d133f46.xml",
        "data/ir_sequence/general_audit_ws_d133f46.xml",
        "data/sequence_template/general_audit_ws_d133f46.xml",
        "data/policy_template/general_audit_ws_d133f46.xml",
        "data/approval_template/general_audit_ws_d133f46.xml",
        "views/ga_d133f46/general_audit_ws_d133f46_views.xml",
        "views/ga_d133f46/general_audit_ws_d133f46_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
