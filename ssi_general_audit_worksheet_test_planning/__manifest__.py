# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Test Planning",
    "version": "14.0.1.4.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_worksheet_romm",
        "ssi_general_audit_worksheet_inherent_risk",
        "ssi_general_audit_worksheet_preliminary_materiality",
        "ssi_general_audit_worksheet_analytic_cycle",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/general_audit_ws_f9a2c3d.xml",
        "security/res_groups/general_audit_ws_f9a2c3d.xml",
        "security/ir_model_access/general_audit_ws_f9a2c3d.xml",
        "security/ir_rule/general_audit_ws_f9a2c3d.xml",
        "data/ir_sequence/general_audit_ws_f9a2c3d.xml",
        "data/sequence_template/general_audit_ws_f9a2c3d.xml",
        "data/policy_template/general_audit_ws_f9a2c3d.xml",
        "data/approval_template/general_audit_ws_f9a2c3d.xml",
        "data/general_audit_worksheet_type/general_audit_ws_f9a2c3d.xml",
        "data/master/general_audit_ws_f9a2c3d_timing.xml",
        "data/master/general_audit_ws_f9a2c3d_extent.xml",
        "data/master/general_audit_ws_f9a2c3d_technique.xml",
        "views/master/general_audit_ws_f9a2c3d_timing_views.xml",
        "views/master/general_audit_ws_f9a2c3d_extent_views.xml",
        "views/master/general_audit_ws_f9a2c3d_technique_views.xml",
        "views/general_audit_ws_f9a2c3d.xml",
        "views/assets.xml",
    ],
    "demo": [],
}
