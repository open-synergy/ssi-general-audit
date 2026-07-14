# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Draft Reporting",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_worksheet_audit_result",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "data/general_audit_worksheet_type_data.xml",
        # MASTER DATA
        "data/master/general_audit_worksheet_conclusion.xml",
        "data/master/general_audit_ws_bbbdfe7_item.xml",
        "data/master/general_audit_ws_de69c2f_item.xml",
        # b555edd - Report Formatting Control
        "security/res_group/general_audit_ws_b555edd.xml",
        "security/ir_rule/general_audit_ws_b555edd.xml",
        "data/ir_sequence/general_audit_ws_b555edd.xml",
        "data/sequence_template/general_audit_ws_b555edd.xml",
        "data/policy_template/general_audit_ws_b555edd.xml",
        "data/approval_template/general_audit_ws_b555edd.xml",
        "views/ga_b555edd/general_audit_ws_b555edd_views.xml",
        # e59c663 - Draft Financial Statements
        "security/res_group/general_audit_ws_e59c663.xml",
        "security/ir_rule/general_audit_ws_e59c663.xml",
        "data/ir_sequence/general_audit_ws_e59c663.xml",
        "data/sequence_template/general_audit_ws_e59c663.xml",
        "data/policy_template/general_audit_ws_e59c663.xml",
        "data/approval_template/general_audit_ws_e59c663.xml",
        "views/ga_e59c663/general_audit_ws_e59c663_views.xml",
        # de69c2f - Final Discussion
        "security/res_group/general_audit_ws_de69c2f.xml",
        "security/ir_rule/general_audit_ws_de69c2f.xml",
        "data/ir_sequence/general_audit_ws_de69c2f.xml",
        "data/sequence_template/general_audit_ws_de69c2f.xml",
        "data/policy_template/general_audit_ws_de69c2f.xml",
        "data/approval_template/general_audit_ws_de69c2f.xml",
        "views/ga_de69c2f/general_audit_ws_de69c2f_views.xml",
        "views/ga_de69c2f/general_audit_ws_de69c2f_item_views.xml",
        # ff42fdc - Audit Result
        "security/res_group/general_audit_ws_ff42fdc.xml",
        "security/ir_rule/general_audit_ws_ff42fdc.xml",
        "data/ir_sequence/general_audit_ws_ff42fdc.xml",
        "data/sequence_template/general_audit_ws_ff42fdc.xml",
        "data/policy_template/general_audit_ws_ff42fdc.xml",
        "data/approval_template/general_audit_ws_ff42fdc.xml",
        "views/ga_ff42fdc/general_audit_ws_ff42fdc_views.xml",
        # ae598e6 - Management Letter
        "security/res_group/general_audit_ws_ae598e6.xml",
        "security/ir_rule/general_audit_ws_ae598e6.xml",
        "data/ir_sequence/general_audit_ws_ae598e6.xml",
        "data/sequence_template/general_audit_ws_ae598e6.xml",
        "data/policy_template/general_audit_ws_ae598e6.xml",
        "data/approval_template/general_audit_ws_ae598e6.xml",
        "views/ga_ae598e6/general_audit_ws_ae598e6_views.xml",
        # bbbdfe7 - Management Representation
        "security/res_group/general_audit_ws_bbbdfe7.xml",
        "security/ir_rule/general_audit_ws_bbbdfe7.xml",
        "data/ir_sequence/general_audit_ws_bbbdfe7.xml",
        "data/sequence_template/general_audit_ws_bbbdfe7.xml",
        "data/policy_template/general_audit_ws_bbbdfe7.xml",
        "data/approval_template/general_audit_ws_bbbdfe7.xml",
        "views/ga_bbbdfe7/general_audit_ws_bbbdfe7_views.xml",
        "views/ga_bbbdfe7/general_audit_ws_bbbdfe7_item_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
