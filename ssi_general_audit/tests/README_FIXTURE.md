# Shared fixture recipe — `general_audit` in state `open`

Every worksheet module (`ssi_general_audit_worksheet_*`) inherits
`general_audit_worksheet_mixin`, which requires a `general_audit_id`. Its unit tests
need a `general_audit` record to attach worksheets to — usually in state `open`
(worksheets are normally created while the audit is in progress). Copy the block below
into a new scenario's `steps:` list and adjust `save_as` aliases if they collide with
your own fixture data.

This recipe deliberately sets `need_interim: false` and `need_previous: false` so
`action_confirm` on the audit does not require extra interim / previous trial balances —
worksheet tests should not need to go past `open` state at all; only copy the "Confirm"
and "Approve" steps too if your scenario specifically needs `general_audit` in state
`done`.

```yaml
- step: "Create client partner"
  action: "create"
  model: "res.partner"
  save_as: "client"
  as_user: "base.user_admin"
  values:
    name: "Test Audit Client"
    is_company: true

- step: "Create accountant partner"
  action: "create"
  model: "res.partner"
  save_as: "accountant"
  as_user: "base.user_admin"
  values:
    name: "Test Audit Accountant"

- step: "Get CPA license id category"
  action: "ref"
  xml_id: "ssi_partner_identification_cpa_license.partner_identification_accountant_cpa_license"
  save_as: "cpa_category"

- step: "Grant accountant a CPA license"
  action: "create"
  model: "res.partner.id_number"
  save_as: "cpa_license"
  as_user: "base.user_admin"
  values:
    partner_id: "EVAL: registry['accountant'].id"
    category_id: "EVAL: registry['cpa_category'].id"
    name: "CPA-<UNIQUE-SUFFIX>"

- step: "Create account type set"
  action: "create"
  model: "client_account_type_set"
  save_as: "account_type_set"
  as_user: "base.user_admin"
  values:
    name: "Test Account Type Set"
    code: "/"

- step: "Create financial accounting standard"
  action: "create"
  model: "accountant.financial_accounting_standard"
  save_as: "standard"
  as_user: "base.user_admin"
  values:
    name: "Test Financial Accounting Standard"
    code: "/"

- step: "Create general audit"
  action: "create"
  model: "general_audit"
  save_as: "audit"
  as_user: "base.user_admin"
  values:
    title: "Test General Audit"
    partner_id: "EVAL: registry['client'].id"
    accountant_id: "EVAL: registry['accountant'].id"
    account_type_set_id: "EVAL: registry['account_type_set'].id"
    financial_accounting_standard_id: "EVAL: registry['standard'].id"
    date_start: 2026-01-01
    date_end: 2026-12-31
    need_interim: false
    need_previous: false
    num_of_consecutive_audit_firm: 1
    num_of_consecutive_audit_accountant: 1

- step: "Open general audit"
  action: "call"
  target: "audit"
  method: "action_open"
  as_user: "base.user_admin"
  asserts:
    state:
      type: "value"
      expected: "open"
```

After this block, `registry['audit']` is a `general_audit` record in state `open` —
create your worksheet against it, e.g.:

```yaml
- step: "Create worksheet"
  action: "create"
  model: "<your_worksheet_model>"
  save_as: "worksheet"
  as_user: "base.user_admin"
  values:
    general_audit_id: "EVAL: registry['audit'].id"
    type_id: "REF: <your_module>.<worksheet_type_xml_id>"
```

## Why `as_user: "base.user_admin"` everywhere

YAML scenarios run as **OdooBot** (`uid=1`) by default. OdooBot is _not_ a member of any
`res.groups` (even though it is superuser), so any policy field derived from group
membership — including `ssi_multiple_approval_mixin`'s `active_approver_user_ids` check
behind `confirm_ok` / `approve_ok` — evaluates to `False` for OdooBot. `Administrator`
(`base.user_admin`) is explicitly added to
`ssi_general_audit.general_audit_validator_group` and
`ssi_general_audit.trial_balance_validator_group` (`security/res_group_data.xml`), so
running every `general_audit` / `client_trial_balance` step as `base.user_admin` lets
`action_open`, `action_confirm`, and `action_approve_approval` all succeed.

## Why you (usually) don't need a trial balance

`general_audit._constrains_state_confirm` requires a **home** trial balance in state
`done` before `action_confirm` succeeds — see `_check_home_tb_exist` /
`_check_home_tb_done` in `models/general_audit/general_audit.py`. That only fires when
the audit itself transitions to `confirm`. Worksheet tests normally only need the audit
in state `open` (as this recipe produces), so they can skip the trial balance fixture
entirely. If a worksheet test genuinely needs the parent audit in state `done`, see the
"Workflow draft to done" scenario in
`ssi_general_audit/tests/test_data_general_audit.yaml` for the full home trial balance
fixture (create → open → confirm → approve).

## `general_audit_worksheet_mixin` is abstract

`general_audit_worksheet_mixin` (`models/worksheet/general_audit_worksheet_mixin.py`) is
a `models.AbstractModel` — it has no table of its own. Concrete worksheet modules
provide their own `models.Model` that does
`_inherit = ["general_audit_worksheet_mixin", ...]` plus a `_type_xml_id` (see
`ssi_general_audit_worksheet_trial_balance/models/general_audit_ws_a033cc6.py` for the
pattern). Since that concrete model is real production code shipped by the worksheet
module, its own tests do **not** need the `odoo_test_helper.FakeModelLoader` trick used
in this module's `test_general_audit.py` — that trick only exists here because
`ssi_general_audit` itself has no concrete worksheet model to test the mixin's
`standard_item_ids` / `allowed_conclusion_ids` compute and `onchange_parent_type_id`
against.
