# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - " "Final Materiality & Analytical Procedures",
    "version": "14.0.1.1.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_worksheet_preliminary_materiality",
        "ssi_general_audit_worksheet_preliminary_analytic_procedure",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # MASTER DATA
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_ws_c2375d8_item.xml",
        # bb33b94 - Final Materiality
        "security/res_group/general_audit_ws_bb33b94.xml",
        "security/ir_rule/general_audit_ws_bb33b94.xml",
        "data/ir_sequence/general_audit_ws_bb33b94.xml",
        "data/sequence_template/general_audit_ws_bb33b94.xml",
        "data/policy_template/general_audit_ws_bb33b94.xml",
        "data/approval_template/general_audit_ws_bb33b94.xml",
        "views/ga_bb33b94/general_audit_ws_bb33b94_views.xml",
        # c2375d8 - Final Analytical Procedures
        "security/res_group/general_audit_ws_c2375d8.xml",
        "security/ir_rule/general_audit_ws_c2375d8.xml",
        "data/ir_sequence/general_audit_ws_c2375d8.xml",
        "data/sequence_template/general_audit_ws_c2375d8.xml",
        "data/policy_template/general_audit_ws_c2375d8.xml",
        "data/approval_template/general_audit_ws_c2375d8.xml",
        "views/ga_c2375d8/general_audit_ws_c2375d8_views.xml",
        "views/ga_c2375d8/general_audit_ws_c2375d8_item_views.xml",
        # e1f2d98 - Final Analytical Procedures - Vertical and Horisontal Analysis
        "security/res_group/general_audit_ws_e1f2d98.xml",
        "security/ir_rule/general_audit_ws_e1f2d98.xml",
        "data/ir_sequence/general_audit_ws_e1f2d98.xml",
        "data/sequence_template/general_audit_ws_e1f2d98.xml",
        "data/policy_template/general_audit_ws_e1f2d98.xml",
        "data/approval_template/general_audit_ws_e1f2d98.xml",
        "views/ga_e1f2d98/general_audit_ws_e1f2d98_views.xml",
        # f3a78de - Final Analytical Procedures - Ratio Analysis
        "security/res_group/general_audit_ws_f3a78de.xml",
        "security/ir_rule/general_audit_ws_f3a78de.xml",
        "data/ir_sequence/general_audit_ws_f3a78de.xml",
        "data/sequence_template/general_audit_ws_f3a78de.xml",
        "data/policy_template/general_audit_ws_f3a78de.xml",
        "data/approval_template/general_audit_ws_f3a78de.xml",
        "views/ga_f3a78de/general_audit_ws_f3a78de_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
