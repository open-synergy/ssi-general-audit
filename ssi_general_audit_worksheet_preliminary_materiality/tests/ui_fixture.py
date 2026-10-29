# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


def create_open_general_audit(env, number):
    """Create a General Audit, open it, and give it a fixed number.

    The tours pick the audit through the UI by its number, because the
    generated one changes on every run.

    :param env: environment used to create the fixture records.
    :param str number: number the audit gets after it is opened.
    :return: the opened ``general_audit`` record.
    """
    # user_id is explicit: env runs as SUPERUSER and record rules would
    # otherwise hide the fixtures from the admin session of the tour.
    admin = env.ref("base.user_admin")
    env["ir.config_parameter"].sudo().set_param(
        "ssi_general_audit.max_number_of_cpa_license", "100"
    )
    client = (
        env["res.partner"]
        .with_user(admin)
        .create({"name": "Test Audit Client - %s" % number, "is_company": True})
    )
    accountant = (
        env["res.partner"]
        .with_user(admin)
        .create({"name": "Test Audit Accountant - %s" % number})
    )
    cpa_category = env.ref(
        "ssi_partner_identification_cpa_license"
        ".partner_identification_accountant_cpa_license"
    )
    env["res.partner.id_number"].with_user(admin).create(
        {
            "partner_id": accountant.id,
            "category_id": cpa_category.id,
            "name": "CPA-%s" % number,
        }
    )
    account_type_set = (
        env["client_account_type_set"]
        .with_user(admin)
        .create({"name": "Test Account Type Set - %s" % number, "code": "/"})
    )
    standard = (
        env["accountant.financial_accounting_standard"]
        .with_user(admin)
        .create({"name": "Test Standard - %s" % number, "code": "/"})
    )
    audit = (
        env["general_audit"]
        .with_user(admin)
        .create(
            {
                "title": "Test General Audit - %s" % number,
                "partner_id": client.id,
                "accountant_id": accountant.id,
                "account_type_set_id": account_type_set.id,
                "financial_accounting_standard_id": standard.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
                "need_interim": False,
                "need_previous": False,
                "num_of_consecutive_audit_firm": 1,
                "num_of_consecutive_audit_accountant": 1,
            }
        )
    )
    audit.with_user(admin).action_open()
    audit.sudo().write({"name": number})
    return audit
