# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Inspection",
    "version": "14.0.1.0.3",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_lead_schedule",
    ],
    "data": [
        "security/ir_module_category/general_audit_ws_c7d5f2b.xml",
        "security/res_groups/general_audit_ws_c7d5f2b.xml",
        "security/ir_model_access/general_audit_ws_c7d5f2b.xml",
        "security/ir_rule/general_audit_ws_c7d5f2b.xml",
        "data/ir_sequence/general_audit_ws_c7d5f2b.xml",
        "data/sequence_template/general_audit_ws_c7d5f2b.xml",
        "data/policy_template/general_audit_ws_c7d5f2b.xml",
        "data/approval_template/general_audit_ws_c7d5f2b.xml",
        "data/general_audit_worksheet_type/general_audit_ws_c7d5f2b.xml",
        "views/general_audit_ws_c7d5f2b_views.xml",
    ],
    "demo": [],
}
