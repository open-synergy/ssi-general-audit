# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet - Draft Reporting",
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
        # b555edd
        "security/res_group/general_audit_ws_b555edd.xml",
        "security/ir_rule/general_audit_ws_b555edd.xml",
        "data/ir_sequence/general_audit_ws_b555edd.xml",
        "data/sequence_template/general_audit_ws_b555edd.xml",
        "data/policy_template/general_audit_ws_b555edd.xml",
        "data/approval_template/general_audit_ws_b555edd.xml",
        "views/general_audit_ws_b555edd_views.xml",
        # e59c663
        "security/res_group/general_audit_ws_e59c663.xml",
        "security/ir_rule/general_audit_ws_e59c663.xml",
        "data/ir_sequence/general_audit_ws_e59c663.xml",
        "data/sequence_template/general_audit_ws_e59c663.xml",
        "data/policy_template/general_audit_ws_e59c663.xml",
        "data/approval_template/general_audit_ws_e59c663.xml",
        "views/general_audit_ws_e59c663_views.xml",
        # de69c2f
        "security/res_group/general_audit_ws_de69c2f.xml",
        "security/ir_rule/general_audit_ws_de69c2f.xml",
        "data/ir_sequence/general_audit_ws_de69c2f.xml",
        "data/sequence_template/general_audit_ws_de69c2f.xml",
        "data/policy_template/general_audit_ws_de69c2f.xml",
        "data/approval_template/general_audit_ws_de69c2f.xml",
        "views/general_audit_ws_de69c2f_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
