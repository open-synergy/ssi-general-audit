# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Lead Schedule",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_control_risk",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # MASTER DATA
        "data/master/general_audit_audit_procedure_category.xml",
        "data/master/general_audit_audit_procedure.xml",
        # b26d482
        "security/res_group/general_audit_ws_b26d482.xml",
        "security/ir_rule/general_audit_ws_b26d482.xml",
        "data/ir_sequence/general_audit_ws_b26d482.xml",
        "data/sequence_template/general_audit_ws_b26d482.xml",
        "data/policy_template/general_audit_ws_b26d482.xml",
        "data/approval_template/general_audit_ws_b26d482.xml",
        "views/general_audit_ws_b26d482_views.xml",
        # e51bb1c
        "security/res_group/general_audit_ws_e51bb1c.xml",
        "security/ir_rule/general_audit_ws_e51bb1c.xml",
        "data/ir_sequence/general_audit_ws_e51bb1c.xml",
        "data/sequence_template/general_audit_ws_e51bb1c.xml",
        "data/policy_template/general_audit_ws_e51bb1c.xml",
        "data/approval_template/general_audit_ws_e51bb1c.xml",
        "views/general_audit_ws_e51bb1c_views.xml",
        # f9f3299
        "security/res_group/general_audit_ws_f9f3299.xml",
        "security/ir_rule/general_audit_ws_f9f3299.xml",
        "data/ir_sequence/general_audit_ws_f9f3299.xml",
        "data/sequence_template/general_audit_ws_f9f3299.xml",
        "data/policy_template/general_audit_ws_f9f3299.xml",
        "data/approval_template/general_audit_ws_f9f3299.xml",
        "views/general_audit_ws_f9f3299_views.xml",
        "security/ir.model.access.csv",
        "views/general_audit_audit_procedure_category_views.xml",
        "views/general_audit_audit_procedure_views.xml",
    ],
    "demo": [],
}
