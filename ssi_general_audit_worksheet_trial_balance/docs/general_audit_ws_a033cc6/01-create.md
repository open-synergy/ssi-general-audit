# Create Trial Balance

> **Module:** `ssi_general_audit_worksheet_trial_balance`\
> **Model:** `general_audit_ws_a033cc6`\
> **Menu:** Risk Assessment > Trial Balance > Trial Balance\
> **Actor:** user in group _Trial Balance (a033cc6) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** Fewer than two `general_audit_ws_a033cc6` worksheets exist for that General
  Audit (at most two of this kind are allowed per General Audit).
- **Access:** User is in group _Trial Balance (a033cc6) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Trial Balance > Trial Balance** menu. If **Trial
   Balance** is not visible in the top menu bar, click the **+** button at its right end
   first. The menu list that opens shows **Trial Balance** with its entry below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
