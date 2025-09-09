# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - " "Final Materiality & Analytical Procedures",
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
        # bb33b94
        "security/res_group/general_audit_ws_bb33b94.xml",
        "security/ir_rule/general_audit_ws_bb33b94.xml",
        "data/ir_sequence/general_audit_ws_bb33b94.xml",
        "data/sequence_template/general_audit_ws_bb33b94.xml",
        "data/policy_template/general_audit_ws_bb33b94.xml",
        "data/approval_template/general_audit_ws_bb33b94.xml",
        "views/general_audit_ws_bb33b94_views.xml",
        # c2375d8
        "security/res_group/general_audit_ws_c2375d8.xml",
        "security/ir_rule/general_audit_ws_c2375d8.xml",
        "data/ir_sequence/general_audit_ws_c2375d8.xml",
        "data/sequence_template/general_audit_ws_c2375d8.xml",
        "data/policy_template/general_audit_ws_c2375d8.xml",
        "data/approval_template/general_audit_ws_c2375d8.xml",
        "views/general_audit_ws_c2375d8_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
