# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Test Planning",
    "version": "14.0.1.1.1",
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
        "views/general_audit_ws_f9a2c3d.xml",
    ],
    "demo": [],
}
