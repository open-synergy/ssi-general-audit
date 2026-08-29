# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Recompute Audit Procedure",
    "version": "14.0.1.2.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_client_package",
        "ssi_general_audit_worksheet_control_risk",
        "ssi_general_audit_worksheet_lead_schedule",
        "ssi_general_audit_worksheet_sample_determination",
        "ssi_general_audit_worksheet_understanding_entity",
        "ssi_web_widget_csv_table",
    ],
    "data": [
        "security/ir_module_category/general_audit_ws_c6c86fd.xml",
        "security/res_groups/general_audit_ws_c6c86fd.xml",
        "security/ir_model_access/general_audit_ws_c6c86fd.xml",
        "security/ir_rule/general_audit_ws_c6c86fd.xml",
        "data/ir_sequence/general_audit_ws_c6c86fd.xml",
        "data/sequence_template/general_audit_ws_c6c86fd.xml",
        "data/policy_template/general_audit_ws_c6c86fd.xml",
        "data/approval_template/general_audit_ws_c6c86fd.xml",
        "data/general_audit_worksheet_type/general_audit_ws_c6c86fd.xml",
        "views/general_audit_ws_c6c86fd.xml",
    ],
    "demo": [],
}
