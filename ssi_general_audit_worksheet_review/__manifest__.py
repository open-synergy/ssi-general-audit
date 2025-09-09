# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Review",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # a025441
        "security/res_group/general_audit_ws_a025441.xml",
        "security/ir_rule/general_audit_ws_a025441.xml",
        "data/ir_sequence/general_audit_ws_a025441.xml",
        "data/sequence_template/general_audit_ws_a025441.xml",
        "data/policy_template/general_audit_ws_a025441.xml",
        "data/approval_template/general_audit_ws_a025441.xml",
        "views/general_audit_ws_a025441_views.xml",
        # bcc0d76
        "security/res_group/general_audit_ws_bcc0d76.xml",
        "security/ir_rule/general_audit_ws_bcc0d76.xml",
        "data/ir_sequence/general_audit_ws_bcc0d76.xml",
        "data/sequence_template/general_audit_ws_bcc0d76.xml",
        "data/policy_template/general_audit_ws_bcc0d76.xml",
        "data/approval_template/general_audit_ws_bcc0d76.xml",
        "views/general_audit_ws_bcc0d76_views.xml",
        # dae9f3c
        "security/res_group/general_audit_ws_dae9f3c.xml",
        "security/ir_rule/general_audit_ws_dae9f3c.xml",
        "data/ir_sequence/general_audit_ws_dae9f3c.xml",
        "data/sequence_template/general_audit_ws_dae9f3c.xml",
        "data/policy_template/general_audit_ws_dae9f3c.xml",
        "data/approval_template/general_audit_ws_dae9f3c.xml",
        "views/general_audit_ws_dae9f3c_views.xml",
        # fc75636
        "security/res_group/general_audit_ws_fc75636.xml",
        "security/ir_rule/general_audit_ws_fc75636.xml",
        "data/ir_sequence/general_audit_ws_fc75636.xml",
        "data/sequence_template/general_audit_ws_fc75636.xml",
        "data/policy_template/general_audit_ws_fc75636.xml",
        "data/approval_template/general_audit_ws_fc75636.xml",
        "views/general_audit_ws_fc75636_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
