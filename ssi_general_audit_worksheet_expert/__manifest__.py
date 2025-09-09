# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Expert",
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
        # bab9d32
        "security/res_group/general_audit_ws_bab9d32.xml",
        "security/ir_rule/general_audit_ws_bab9d32.xml",
        "data/ir_sequence/general_audit_ws_bab9d32.xml",
        "data/sequence_template/general_audit_ws_bab9d32.xml",
        "data/policy_template/general_audit_ws_bab9d32.xml",
        "data/approval_template/general_audit_ws_bab9d32.xml",
        "views/general_audit_ws_bab9d32_views.xml",
        # cda3a68
        "security/res_group/general_audit_ws_cda3a68.xml",
        "security/ir_rule/general_audit_ws_cda3a68.xml",
        "data/ir_sequence/general_audit_ws_cda3a68.xml",
        "data/sequence_template/general_audit_ws_cda3a68.xml",
        "data/policy_template/general_audit_ws_cda3a68.xml",
        "data/approval_template/general_audit_ws_cda3a68.xml",
        "views/general_audit_ws_cda3a68_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
