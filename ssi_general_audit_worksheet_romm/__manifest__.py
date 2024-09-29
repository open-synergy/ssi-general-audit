# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - ROMM",
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
        "security/res_group/general_audit_ws_c165170.xml",
        "security/res_group/general_audit_ws_d66d87a.xml",
        "security/ir_model_access/general_audit_ws_c165170.xml",
        "security/ir_model_access/general_audit_ws_d66d87a.xml",
        "security/ir_rule/general_audit_ws_c165170.xml",
        "security/ir_rule/general_audit_ws_d66d87a.xml",
        "data/ir_sequence/general_audit_ws_c165170.xml",
        "data/ir_sequence/general_audit_ws_d66d87a.xml",
        "data/sequence_template/general_audit_ws_c165170.xml",
        "data/sequence_template/general_audit_ws_d66d87a.xml",
        "data/policy_template/general_audit_ws_c165170.xml",
        "data/policy_template/general_audit_ws_d66d87a.xml",
        "data/approval_template/general_audit_ws_c165170.xml",
        "data/approval_template/general_audit_ws_d66d87a.xml",
        "data/general_audit_worksheet_type_data.xml",
        "views/general_audit_ws_c165170_views.xml",
        "views/general_audit_ws_d66d87a_views.xml",
        "views/general_audit_standard_detail_views.xml",
    ],
    "demo": [],
}
