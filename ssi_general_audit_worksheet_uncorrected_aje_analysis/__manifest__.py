# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Uncorrected AJE Analysis",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_preliminary_materiality",
    ],
    "data": [
        "security/ir_module_category/general_audit_ws_c3b9e71.xml",
        "security/res_groups/general_audit_ws_c3b9e71.xml",
        "security/ir_model_access/general_audit_ws_c3b9e71.xml",
        "security/ir_rule/general_audit_ws_c3b9e71.xml",
        "data/ir_sequence/general_audit_ws_c3b9e71.xml",
        "data/sequence_template/general_audit_ws_c3b9e71.xml",
        "data/policy_template/general_audit_ws_c3b9e71.xml",
        "data/approval_template/general_audit_ws_c3b9e71.xml",
        "data/general_audit_worksheet_type/general_audit_ws_c3b9e71.xml",
        "views/client_adjustment_entry_readonly.xml",
        "views/general_audit_ws_c3b9e71.xml",
    ],
    "demo": [],
}
