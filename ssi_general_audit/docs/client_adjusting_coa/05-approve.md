# Approve Adjusting CoA

> **Module:** `ssi_general_audit`\
> **Model:** `client_adjusting_coa`\
> **Menu:** Risk Responses > Result > Adjusting CoA\
> **Actor:** Approver on the pending approval level\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor.
- **Access:** User is registered as an approver on the approval level that is currently
  pending.
- **Access:** User has _Can Approve_ access right.

## Flow

1. Open the **Risk Responses > Result > Adjusting CoA** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- When all approval levels are fulfilled, status changes to **Done**.
- A client account is created for each line, and the account is shown on the line.
- The accounts are added to the General Audit and appear in **GA-Account**, with zero
  balance. Worksheets from **Worksheet** onwards receive them; earlier worksheets,
  including **Lead Schedules**, do not.
- A Done document cannot be cancelled.
