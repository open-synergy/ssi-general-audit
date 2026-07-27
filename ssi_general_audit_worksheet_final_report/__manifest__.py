# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Final Report",
    "version": "14.0.1.1.1",
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
        # a8c54f3
        "security/res_group/general_audit_ws_a8c54f3.xml",
        "security/ir_rule/general_audit_ws_a8c54f3.xml",
        "data/ir_sequence/general_audit_ws_a8c54f3.xml",
        "data/sequence_template/general_audit_ws_a8c54f3.xml",
        "data/policy_template/general_audit_ws_a8c54f3.xml",
        "data/approval_template/general_audit_ws_a8c54f3.xml",
        "views/general_audit_ws_a8c54f3_views.xml",
        # b66777d
        "security/res_group/general_audit_ws_b66777d.xml",
        "security/ir_rule/general_audit_ws_b66777d.xml",
        "data/ir_sequence/general_audit_ws_b66777d.xml",
        "data/sequence_template/general_audit_ws_b66777d.xml",
        "data/policy_template/general_audit_ws_b66777d.xml",
        "data/approval_template/general_audit_ws_b66777d.xml",
        "views/general_audit_ws_b66777d_views.xml",
        # f3ed115
        "security/res_group/general_audit_ws_f3ed115.xml",
        "security/ir_rule/general_audit_ws_f3ed115.xml",
        "data/ir_sequence/general_audit_ws_f3ed115.xml",
        "data/sequence_template/general_audit_ws_f3ed115.xml",
        "data/policy_template/general_audit_ws_f3ed115.xml",
        "data/approval_template/general_audit_ws_f3ed115.xml",
        "views/general_audit_ws_f3ed115_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
