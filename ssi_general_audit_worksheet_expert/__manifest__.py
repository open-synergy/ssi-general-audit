# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Expert",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_understanding_entity",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        "templates/expert_templates.xml",
        # Master Data
        "data/master/general_audit_ws_bab9d32_category.xml",
        "data/master/general_audit_ws_bab9d32_factor.xml",
        "data/master/general_audit_ws_cda3a68_category.xml",
        "data/master/general_audit_ws_cda3a68_factor.xml",
        # bab9d32 - Auditor Expert
        "security/res_group/general_audit_ws_bab9d32.xml",
        "security/ir_rule/general_audit_ws_bab9d32.xml",
        "data/ir_sequence/general_audit_ws_bab9d32.xml",
        "data/sequence_template/general_audit_ws_bab9d32.xml",
        "data/policy_template/general_audit_ws_bab9d32.xml",
        "data/approval_template/general_audit_ws_bab9d32.xml",
        "views/ga_bab9d32/general_audit_ws_bab9d32_category_views.xml",
        "views/ga_bab9d32/general_audit_ws_bab9d32_factor_views.xml",
        "views/ga_bab9d32/general_audit_ws_bab9d32_views.xml",
        # cda3a68 - Management Expert
        "security/res_group/general_audit_ws_cda3a68.xml",
        "security/ir_rule/general_audit_ws_cda3a68.xml",
        "data/ir_sequence/general_audit_ws_cda3a68.xml",
        "data/sequence_template/general_audit_ws_cda3a68.xml",
        "data/policy_template/general_audit_ws_cda3a68.xml",
        "data/approval_template/general_audit_ws_cda3a68.xml",
        "views/ga_cda3a68/general_audit_ws_cda3a68_views.xml",
        "views/ga_cda3a68/general_audit_ws_cda3a68_category_views.xml",
        "views/ga_cda3a68/general_audit_ws_cda3a68_factor_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
