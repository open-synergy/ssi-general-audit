# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Preliminary Materiality",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        # Approval Template
        "data/approval_template/general_audit_ws_1d9338d.xml",
        "data/approval_template/general_audit_ws_d9d2b44.xml",
        "data/approval_template/general_audit_ws_6dcda0e.xml",
        "data/general_audit_worksheet_type_data.xml",
        # Policy Template
        "data/policy_template/general_audit_ws_6dcda0e.xml",
        "data/policy_template/general_audit_ws_d9d2b44.xml",
        "data/policy_template/general_audit_ws_1d9338d.xml",
        # Sequence Template
        # MASTER DATA
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_ws_1d9338d_item.xml",
        # 6dcda0e - Specific Materiality
        "views/ga_6dcda0e/general_audit_ws_6dcda0e_views.xml",
        # d9d2b44 - Materiality Computation
        "views/ga_d9d2b44/general_audit_ws_d9d2b44_views.xml",
        # 1d9338d - Preliminary Materiality
        "security/res_group/general_audit_ws_1d9338d.xml",
        "security/ir_rule/general_audit_ws_1d9338d.xml",
        "data/ir_sequence/general_audit_ws_1d9338d.xml",
        "data/sequence_template/general_audit_ws_1d9338d.xml",
        "data/approval_template/general_audit_ws_1d9338d.xml",
        "views/ga_1d9338d/general_audit_ws_1d9338d_views.xml",
        "views/ga_1d9338d/general_audit_ws_1d9338d_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
