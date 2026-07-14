# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged("post_install", "-at_install")
class TestGeneralAuditWSd9d2b44(YamlTransactionCase):
    def test_general_audit_ws_d9d2b44(self):
        self.run_yaml_scenario("test_data_general_audit_ws_d9d2b44.yaml")

    def test_onchange_type_id_updates_worksheet(self):
        """``type_id`` (``general_audit_worksheet_mixin``) defaults from
        ``_type_xml_id`` and is force-readonly (``readonly=True``, only
        writable while ``state == "draft"`` per its ``states`` dict, and not
        reachable through ``.create()``/``.write()`` since those bypass
        onchange entirely). The only way to observe
        ``onchange_parent_type_id`` firing for that defaulted value is a bare
        ``Form()`` on a brand-new record -- this cannot be expressed as a
        YAML ``action: form`` because asserting fields directly on the
        pending (unsaved) form hits a known ``odoo_yaml_test`` bug
        (``hasattr(form, "__len__")`` triggers ``Form.__getattr__``'s own
        ``AssertionError`` before the real assertion runs).

        Deliberately not using ``with Form(...) as form:`` -- the context
        manager calls ``save()`` on ``__exit__``, which would fail here
        because ``general_audit_id`` (a real required field) is never
        filled; this test only cares about the pending onchange state,
        matching the proven pattern already used by
        ``ssi_general_audit_worksheet_expert``'s
        ``test_onchange_type_id_sets_parent_type_id``.
        """
        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_preliminary_materiality."
            "worksheet_type_d9d2b44"
        )
        form = Form(self.env["general_audit_ws_d9d2b44"])
        self.assertEqual(form.type_id, ws_type)
        self.assertEqual(form.parent_type_id, ws_type)
        # standard_item_ids / allowed_conclusion_ids
        # (general_audit_worksheet_mixin, store=False) also refresh from the
        # same onchange for the defaulted type_id.
        self.assertEqual(
            set(form.standard_item_ids.ids), set(ws_type.standard_item_ids.ids)
        )
        conclusion = self.env.ref(
            "ssi_general_audit_worksheet_preliminary_materiality."
            "general_audit_worksheet_conclusion_36_e8b65c56"
        )
        self.assertIn(conclusion, form.allowed_conclusion_ids)

    def test_allowed_computation_item_ids_limits_selection(self):
        """``allowed_computation_item_ids`` (``store=False``, depends only on
        ``general_audit_id``) is used by the form view purely as a
        ``domain="[('id', 'in', allowed_computation_item_ids)]"`` filter for
        the ``computation_item_id`` widget (see
        ``views/ga_d9d2b44/general_audit_ws_d9d2b44_views.xml``) -- there is
        no Python-level constraint enforcing it on ``create``/``write``, so
        the restriction can only be observed by inspecting the Form's
        computed value, which requires the Form API.

        ``computation_item_id`` is itself ``readonly=True`` except while the
        *worksheet's own* ``state == "open"`` (see ``states=`` on the field
        in ``general_audit_ws_d9d2b44.py``) -- not the linked general
        audit's state. The worksheet record is therefore created and opened
        via plain ORM calls FIRST, and only THEN wrapped in ``Form(record)``
        (the existing-record constructor, not ``Form(self.env[model_name])``
        which would build a brand-new draft record and keep the field
        readonly regardless of what the general audit's state is).

        Every workflow-policy-gated step runs ``as_user`` ``base.user_admin``
        -- same reason as everywhere else in this module's YAML fixtures
        (``README_FIXTURE.md``): the default test user (OdooBot, uid=1) is
        not a member of any ``res.groups``, so ``open_ok`` would evaluate
        ``False`` for it.
        """
        admin = self.env.ref("base.user_admin")
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("ssi_general_audit.max_number_of_cpa_license", "100")

        client = (
            self.env["res.partner"]
            .with_user(admin)
            .create(
                {"name": "Test Audit Client - Form Allowed Comp", "is_company": True}
            )
        )
        accountant = (
            self.env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Audit Accountant - Form Allowed Comp"})
        )
        cpa_category = self.env.ref(
            "ssi_partner_identification_cpa_license."
            "partner_identification_accountant_cpa_license"
        )
        self.env["res.partner.id_number"].with_user(admin).create(
            {
                "partner_id": accountant.id,
                "category_id": cpa_category.id,
                "name": "CPA-FORM-ALLOWED-COMP-0001",
            }
        )
        account_type_set = (
            self.env["client_account_type_set"]
            .with_user(admin)
            .create({"name": "Test Account Type Set - Form Allowed Comp", "code": "/"})
        )
        standard = (
            self.env["accountant.financial_accounting_standard"]
            .with_user(admin)
            .create({"name": "Test Standard - Form Allowed Comp", "code": "/"})
        )
        audit = (
            self.env["general_audit"]
            .with_user(admin)
            .create(
                {
                    "title": "Test General Audit - Form Allowed Comp",
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
        audit.invalidate_cache()

        comp_item_allowed = (
            self.env["trial_balance_computation_item"]
            .with_user(admin)
            .create({"name": "Allowed Computation Item", "code": "/"})
        )
        comp_item_other = (
            self.env["trial_balance_computation_item"]
            .with_user(admin)
            .create(
                {"name": "Other Computation Item (not linked to audit)", "code": "/"}
            )
        )
        self.env["general_audit.computation"].with_user(admin).create(
            {
                "general_audit_id": audit.id,
                "computation_item_id": comp_item_allowed.id,
                "extrapolation_amount": 100.0,
            }
        )

        ws_type = self.env.ref(
            "ssi_general_audit_worksheet_preliminary_materiality."
            "worksheet_type_d9d2b44"
        )
        record = (
            self.env["general_audit_ws_d9d2b44"]
            .with_user(admin)
            .create(
                {
                    "general_audit_id": audit.id,
                    "type_id": ws_type.id,
                    "other_base_amount": 0.0,
                }
            )
        )
        record.with_user(admin).action_open()
        record.invalidate_cache()
        self.assertEqual(record.state, "open")

        form = Form(record.with_user(admin))
        self.assertIn(comp_item_allowed, form.allowed_computation_item_ids)
        self.assertNotIn(comp_item_other, form.allowed_computation_item_ids)

        # Within the allowed set, and now that the worksheet itself is
        # "open", the widget accepts the assignment.
        form.computation_item_id = comp_item_allowed
        self.assertEqual(form.computation_item_id, comp_item_allowed)
        form.save()
