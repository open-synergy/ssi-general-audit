# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Client Assistance Package",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_web_widget_csv_table",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/ir_module_category/general_audit_ws_d209914.xml",
        "security/ir_module_category/general_audit_ws_b5e3d9f.xml",
        # res.groups
        "security/res_group/general_audit_ws_abd82ed.xml",
        "security/res_group/general_audit_ws_e301171.xml",
        "security/res_group/general_audit_ws_f5a3cee.xml",
        "security/res_group/general_audit_ws_d209914.xml",
        "security/res_group/general_audit_ws_b5e3d9f.xml",
        # ir.model.access
        "security/ir.model.access.csv",
        "security/ir_model_access/general_audit_ws_d209914.xml",
        "security/ir_model_access/general_audit_ws_b5e3d9f.xml",
        # ir.rule
        "security/ir_rule/general_audit_ws_abd82ed.xml",
        "security/ir_rule/general_audit_ws_e301171.xml",
        "security/ir_rule/general_audit_ws_f5a3cee.xml",
        "security/ir_rule/general_audit_ws_d209914.xml",
        "security/ir_rule/general_audit_ws_b5e3d9f.xml",
        # approval_template
        "data/approval_template/general_audit_ws_d209914.xml",
        "data/approval_template/general_audit_ws_abd82ed.xml",
        "data/approval_template/general_audit_ws_f5a3cee.xml",
        "data/approval_template/general_audit_ws_e301171.xml",
        "data/approval_template/general_audit_ws_b5e3d9f.xml",
        # ir.sequence
        "data/ir_sequence/general_audit_ws_abd82ed.xml",
        "data/ir_sequence/general_audit_ws_e301171.xml",
        "data/ir_sequence/general_audit_ws_f5a3cee.xml",
        "data/ir_sequence/general_audit_ws_d209914.xml",
        "data/ir_sequence/general_audit_ws_b5e3d9f.xml",
        # sequence_template
        "data/sequence_template/general_audit_ws_abd82ed.xml",
        "data/sequence_template/general_audit_ws_e301171.xml",
        "data/sequence_template/general_audit_ws_f5a3cee.xml",
        "data/sequence_template/general_audit_ws_d209914.xml",
        "data/sequence_template/general_audit_ws_b5e3d9f.xml",
        # policy_template
        "data/policy_template/general_audit_ws_abd82ed.xml",
        "data/policy_template/general_audit_ws_e301171.xml",
        "data/policy_template/general_audit_ws_f5a3cee.xml",
        "data/policy_template/general_audit_ws_d209914.xml",
        "data/policy_template/general_audit_ws_b5e3d9f.xml",
        # MASTER DATA
        "data/general_audit_worksheet_type_data.xml",
        "data/general_audit_worksheet_type_data/general_audit_ws_d209914.xml",
        "data/general_audit_worksheet_type_data/general_audit_ws_b5e3d9f.xml",
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_ws_e301171_item.xml",
        "data/master/general_audit_ws_abd82ed_item.xml",
        # ir.ui.view
        "views/ga_abd82ed/general_audit_ws_abd82ed_views.xml",
        "views/ga_abd82ed/general_audit_ws_abd82ed_item_views.xml",
        "views/ga_e301171/general_audit_ws_e301171_views.xml",
        "views/ga_e301171/general_audit_ws_e301171_item_views.xml",
        "views/ga_f5a3cee/general_audit_ws_f5a3cee_views.xml",
        "views/general_audit_ws_d209914.xml",
        "views/general_audit_ws_b5e3d9f.xml",
    ],
    "demo": [],
}
