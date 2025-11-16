# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Audit Result",
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
        # a0319a2 - Findings That Influence Opinion
        "security/res_group/general_audit_ws_a0319a2.xml",
        "security/ir_rule/general_audit_ws_a0319a2.xml",
        "data/ir_sequence/general_audit_ws_a0319a2.xml",
        "data/sequence_template/general_audit_ws_a0319a2.xml",
        "data/policy_template/general_audit_ws_a0319a2.xml",
        "data/approval_template/general_audit_ws_a0319a2.xml",
        "views/general_audit_ws_a0319a2_views.xml",
        # d33420f - Control Deficiencies
        "security/res_group/general_audit_ws_d33420f.xml",
        "security/ir_rule/general_audit_ws_d33420f.xml",
        "data/ir_sequence/general_audit_ws_d33420f.xml",
        "data/sequence_template/general_audit_ws_d33420f.xml",
        "data/policy_template/general_audit_ws_d33420f.xml",
        "data/approval_template/general_audit_ws_d33420f.xml",
        "views/general_audit_ws_d33420f_views.xml",
        # ab19fd4 - Audit Result Formulation
        "security/res_group/general_audit_ws_ab19fd4.xml",
        "security/ir_rule/general_audit_ws_ab19fd4.xml",
        "data/ir_sequence/general_audit_ws_ab19fd4.xml",
        "data/sequence_template/general_audit_ws_ab19fd4.xml",
        "data/policy_template/general_audit_ws_ab19fd4.xml",
        "data/approval_template/general_audit_ws_ab19fd4.xml",
        "views/general_audit_ws_ab19fd4_views.xml",
        # bc3e272 - Audit Result Discussion
        "security/res_group/general_audit_ws_bc3e272.xml",
        "security/ir_rule/general_audit_ws_bc3e272.xml",
        "data/ir_sequence/general_audit_ws_bc3e272.xml",
        "data/sequence_template/general_audit_ws_bc3e272.xml",
        "data/policy_template/general_audit_ws_bc3e272.xml",
        "data/approval_template/general_audit_ws_bc3e272.xml",
        "views/general_audit_ws_bc3e272_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
