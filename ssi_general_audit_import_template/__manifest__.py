# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit - Import Template",
    "version": "14.0.1.0.1",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_general_audit",
        "web_tour",
    ],
    "data": [
        "security/res_groups/general_audit_import_template.xml",
        "security/ir_model_access/general_audit_import_template.xml",
        "security/ir_model_access/general_audit_import_template_line.xml",
        "views/general_audit_import_template_views.xml",
        "views/assets.xml",
        "data/general_audit_import_template_data.xml",
    ],
    "demo": [],
}
