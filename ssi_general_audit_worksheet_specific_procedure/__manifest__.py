# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Specific Procedures",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "ssi_general_audit_worksheet_understanding_entity",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # a8f4d88
        "security/res_group/general_audit_ws_a8f4d88.xml",
        "security/ir_rule/general_audit_ws_a8f4d88.xml",
        "data/ir_sequence/general_audit_ws_a8f4d88.xml",
        "data/sequence_template/general_audit_ws_a8f4d88.xml",
        "data/policy_template/general_audit_ws_a8f4d88.xml",
        "data/approval_template/general_audit_ws_a8f4d88.xml",
        "views/general_audit_ws_a8f4d88_views.xml",
        # c40cfd9
        "security/res_group/general_audit_ws_c40cfd9.xml",
        "security/ir_rule/general_audit_ws_c40cfd9.xml",
        "data/ir_sequence/general_audit_ws_c40cfd9.xml",
        "data/sequence_template/general_audit_ws_c40cfd9.xml",
        "data/policy_template/general_audit_ws_c40cfd9.xml",
        "data/approval_template/general_audit_ws_c40cfd9.xml",
        "views/general_audit_ws_c40cfd9_views.xml",
        # cb82c5f
        "security/res_group/general_audit_ws_cb82c5f.xml",
        "security/ir_rule/general_audit_ws_cb82c5f.xml",
        "data/ir_sequence/general_audit_ws_cb82c5f.xml",
        "data/sequence_template/general_audit_ws_cb82c5f.xml",
        "data/policy_template/general_audit_ws_cb82c5f.xml",
        "data/approval_template/general_audit_ws_cb82c5f.xml",
        "views/general_audit_ws_cb82c5f_views.xml",
        # fbf57ee
        "security/res_group/general_audit_ws_fbf57ee.xml",
        "security/ir_rule/general_audit_ws_fbf57ee.xml",
        "data/ir_sequence/general_audit_ws_fbf57ee.xml",
        "data/sequence_template/general_audit_ws_fbf57ee.xml",
        "data/policy_template/general_audit_ws_fbf57ee.xml",
        "data/approval_template/general_audit_ws_fbf57ee.xml",
        "views/general_audit_ws_fbf57ee_views.xml",
        # ee819ae
        "security/res_group/general_audit_ws_ee819ae.xml",
        "security/ir_rule/general_audit_ws_ee819ae.xml",
        "data/ir_sequence/general_audit_ws_ee819ae.xml",
        "data/sequence_template/general_audit_ws_ee819ae.xml",
        "data/policy_template/general_audit_ws_ee819ae.xml",
        "data/approval_template/general_audit_ws_ee819ae.xml",
        "views/general_audit_ws_ee819ae_views.xml",
        "security/ir.model.access.csv",
        "views/general_audit_accounting_estimation_method_views.xml",
        "views/general_audit_accounting_estimation_relevant_control_views.xml",
        "views/general_audit_subsequent_event_views.xml",
        "views/general_audit_related_party_confirmation_procedure_views.xml",
    ],
    "demo": [],
}
