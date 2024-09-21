# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Control Risk",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_worksheet_understanding_entity",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_group/general_audit_ws_d3d2719.xml",
        "security/ir_model_access/general_audit_ws_d3d2719.xml",
        "security/ir_rule/general_audit_ws_d3d2719.xml",
        "data/ir_sequence/general_audit_ws_d3d2719.xml",
        "data/sequence_template/general_audit_ws_d3d2719.xml",
        "data/policy_template/general_audit_ws_d3d2719.xml",
        "data/approval_template/general_audit_ws_d3d2719.xml",
        "data/general_audit_worksheet_type_data.xml",
        "menu.xml",
        "views/general_audit_general_control_category_views.xml",
        "views/general_audit_general_control_views.xml",
        "views/general_audit_general_control_indicator_views.xml",
        "views/general_audit_general_control_set_views.xml",
        "views/general_audit_ws_d3d2719_views.xml",
    ],
    "demo": [],
}
