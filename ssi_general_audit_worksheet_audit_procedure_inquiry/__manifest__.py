# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Inquiry Audit Procedure",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_control_risk",
        "ssi_general_audit_worksheet_lead_schedule",
    ],
    "data": [
        "security/ir_module_category/general_audit_ws_a145276.xml",
        "security/res_groups/general_audit_ws_a145276.xml",
        "security/ir_model_access/general_audit_ws_a145276.xml",
        "security/ir_rule/general_audit_ws_a145276.xml",
        "data/ir_sequence/general_audit_ws_a145276.xml",
        "data/sequence_template/general_audit_ws_a145276.xml",
        "data/policy_template/general_audit_ws_a145276.xml",
        "data/approval_template/general_audit_ws_a145276.xml",
        "data/general_audit_worksheet_type/general_audit_ws_a145276.xml",
        "views/general_audit_ws_a145276_views.xml",
    ],
    "demo": [],
}
