# Confirm Adjusting CoA

> **Module:** `ssi_general_audit`\
> **Model:** `client_adjusting_coa`\
> **Menu:** Risk Responses > Result > Adjusting CoA\
> **Actor:** Responsible user, reviewer, or audit responsible user\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, with at least one line on the **Details** tab.
- **Data:** No line uses a code that already exists for the client, and no code is used
  on two lines.
- **Data:** The type of every line belongs to the account type set of the General Audit.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User has _Can Confirm_ access right.

## Flow

1. Open the **Risk Responses > Result > Adjusting CoA** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
