# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit - Import Template Worksheet",
    "version": "14.0.1.1.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit_import_template",
        "ssi_general_audit_worksheet_client_package",
        "ssi_general_audit_worksheet_population",
        "ssi_general_audit_worksheet_review",
    ],
    "data": [
        "data/general_audit_import_template_data.xml",
        "data/general_audit_import_template_server_action.xml",
    ],
    "demo": [],
}
