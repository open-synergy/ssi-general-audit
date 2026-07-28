# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Inherent Risk",
    "version": "14.0.2.3.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_worksheet_understanding_entity",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/res_group/general_audit_ws_a418d89.xml",
        "security/res_group/general_audit_ws_c16abd7.xml",
        "security/ir_model_access/general_audit_ws_a418d89.xml",
        "security/ir_model_access/general_audit_ws_c16abd7.xml",
        "security/ir_rule/general_audit_ws_a418d89.xml",
        "security/ir_rule/general_audit_ws_c16abd7.xml",
        "data/ir_sequence/general_audit_ws_a418d89.xml",
        "data/ir_sequence/general_audit_ws_c16abd7.xml",
        "data/sequence_template/general_audit_ws_a418d89.xml",
        "data/sequence_template/general_audit_ws_c16abd7.xml",
        "data/policy_template/general_audit_ws_a418d89.xml",
        "data/policy_template/general_audit_ws_c16abd7.xml",
        "data/approval_template/general_audit_ws_a418d89.xml",
        "data/approval_template/general_audit_ws_c16abd7.xml",
        "data/general_audit_worksheet_type_data.xml",
        # MASTER DATA
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_inherent_risk_factor.xml",
        "data/master/general_audit_ws_bfb6dae_item.xml",
        "views/general_audit_inherent_risk_factor_views.xml",
        "views/general_audit_ws_a418d89_views.xml",
        "views/general_audit_ws_c16abd7_views.xml",
        "views/general_audit_standard_detail_views.xml",
        "views/general_audit_views.xml",
        # bfb6dae
        "security/res_group/general_audit_ws_bfb6dae.xml",
        "security/ir_rule/general_audit_ws_bfb6dae.xml",
        "data/ir_sequence/general_audit_ws_bfb6dae.xml",
        "data/sequence_template/general_audit_ws_bfb6dae.xml",
        "data/policy_template/general_audit_ws_bfb6dae.xml",
        "data/approval_template/general_audit_ws_bfb6dae.xml",
        "views/ga_bfb6dae/general_audit_ws_bfb6dae_views.xml",
        "views/ga_bfb6dae/general_audit_ws_bfb6dae_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
