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
        # MASTER DATA
        "data/master/general_audit_ws_be62e79_item.xml",
        "data/master/general_audit_ws_dae9f3c_item.xml",
        "data/master/general_audit_ws_fc75636_category.xml",
        "data/master/general_audit_ws_fc75636_item.xml",
        # be62e79 - Financial Statement Disclosure Review
        "security/res_group/general_audit_ws_be62e79.xml",
        "security/ir_rule/general_audit_ws_be62e79.xml",
        "data/ir_sequence/general_audit_ws_be62e79.xml",
        "data/sequence_template/general_audit_ws_be62e79.xml",
        "data/policy_template/general_audit_ws_be62e79.xml",
        "data/approval_template/general_audit_ws_be62e79.xml",
        "views/ga_be62e79/general_audit_ws_be62e79_views.xml",
        "views/ga_be62e79/general_audit_ws_be62e79_item_views.xml",
        # a025441 - Financial Statement Disclosure
        "security/res_group/general_audit_ws_a025441.xml",
        "security/ir_rule/general_audit_ws_a025441.xml",
        "data/ir_sequence/general_audit_ws_a025441.xml",
        "data/sequence_template/general_audit_ws_a025441.xml",
        "data/policy_template/general_audit_ws_a025441.xml",
        "data/approval_template/general_audit_ws_a025441.xml",
        "views/ga_a025441/general_audit_ws_a025441_views.xml",
        "views/ga_a025441/general_audit_ws_a025441_item_views.xml",
        # bcc0d76 - Audit Quality
        "security/res_group/general_audit_ws_bcc0d76.xml",
        "security/ir_rule/general_audit_ws_bcc0d76.xml",
        "data/ir_sequence/general_audit_ws_bcc0d76.xml",
        "data/sequence_template/general_audit_ws_bcc0d76.xml",
        "data/policy_template/general_audit_ws_bcc0d76.xml",
        "data/approval_template/general_audit_ws_bcc0d76.xml",
        "views/ga_bcc0d76/general_audit_ws_bcc0d76_views.xml",
        # dae9f3c - Audit Evidence Evaluation
        "security/res_group/general_audit_ws_dae9f3c.xml",
        "security/ir_rule/general_audit_ws_dae9f3c.xml",
        "data/ir_sequence/general_audit_ws_dae9f3c.xml",
        "data/sequence_template/general_audit_ws_dae9f3c.xml",
        "data/policy_template/general_audit_ws_dae9f3c.xml",
        "data/approval_template/general_audit_ws_dae9f3c.xml",
        "views/ga_dae9f3c/general_audit_ws_dae9f3c_views.xml",
        "views/ga_dae9f3c/general_audit_ws_dae9f3c_item_views.xml",
        # cae598e - Audit Evidence Evaluation Detail
        "security/res_group/general_audit_ws_cae598e.xml",
        "security/ir_rule/general_audit_ws_cae598e.xml",
        "data/ir_sequence/general_audit_ws_cae598e.xml",
        "data/sequence_template/general_audit_ws_cae598e.xml",
        "data/policy_template/general_audit_ws_cae598e.xml",
        "data/approval_template/general_audit_ws_cae598e.xml",
        "views/ga_cae598e/general_audit_ws_cae598e_views.xml",
        # fc75636 - Independen Auditor Report
        "security/res_group/general_audit_ws_fc75636.xml",
        "security/ir_rule/general_audit_ws_fc75636.xml",
        "data/ir_sequence/general_audit_ws_fc75636.xml",
        "data/sequence_template/general_audit_ws_fc75636.xml",
        "data/policy_template/general_audit_ws_fc75636.xml",
        "data/approval_template/general_audit_ws_fc75636.xml",
        "views/ga_fc75636/general_audit_ws_fc75636_views.xml",
        "views/ga_fc75636/general_audit_ws_fc75636_item_views.xml",
        "views/ga_fc75636/general_audit_ws_fc75636_category_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
