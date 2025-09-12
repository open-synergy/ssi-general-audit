# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Client Assistance Package",
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
        # abd82ed - Client Assistance Package
        "security/res_group/general_audit_ws_abd82ed.xml",
        "security/ir_rule/general_audit_ws_abd82ed.xml",
        "data/ir_sequence/general_audit_ws_abd82ed.xml",
        "data/sequence_template/general_audit_ws_abd82ed.xml",
        "data/policy_template/general_audit_ws_abd82ed.xml",
        "data/approval_template/general_audit_ws_abd82ed.xml",
        "views/general_audit_ws_abd82ed_views.xml",
        # e301171 - Journal Entry Testing
        "security/res_group/general_audit_ws_e301171.xml",
        "security/ir_rule/general_audit_ws_e301171.xml",
        "data/ir_sequence/general_audit_ws_e301171.xml",
        "data/sequence_template/general_audit_ws_e301171.xml",
        "data/policy_template/general_audit_ws_e301171.xml",
        "data/approval_template/general_audit_ws_e301171.xml",
        "views/general_audit_ws_e301171_views.xml",
        # f5a3cee
        "security/res_group/general_audit_ws_f5a3cee.xml",
        "security/ir_rule/general_audit_ws_f5a3cee.xml",
        "data/ir_sequence/general_audit_ws_f5a3cee.xml",
        "data/sequence_template/general_audit_ws_f5a3cee.xml",
        "data/policy_template/general_audit_ws_f5a3cee.xml",
        "data/approval_template/general_audit_ws_f5a3cee.xml",
        "views/general_audit_ws_f5a3cee_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
