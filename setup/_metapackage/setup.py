import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-general-audit",
    description="Meta package for open-synergy-ssi-general-audit Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_general_audit',
        'odoo14-addon-ssi_general_audit_worksheet_control_risk',
        'odoo14-addon-ssi_general_audit_worksheet_inherent_risk',
        'odoo14-addon-ssi_general_audit_worksheet_planning_memorandum',
        'odoo14-addon-ssi_general_audit_worksheet_preliminary_analytic_procedure',
        'odoo14-addon-ssi_general_audit_worksheet_preliminary_materiality',
        'odoo14-addon-ssi_general_audit_worksheet_romm',
        'odoo14-addon-ssi_general_audit_worksheet_understanding_entity',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
