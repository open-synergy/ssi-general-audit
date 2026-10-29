# Create Know Your Customer Principles

> **Module:** `ssi_general_audit_worksheet_acceptance_continuance`\
> **Model:** `general_audit_ws_805d4d5`\
> **Menu:** Pre-Engagement > Client Acceptance > Management Integrity > Know Your
> Customer Principles\
> **Actor:** user in group _Know Your Customer Principles (805d4d5) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_805d4d5` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Know Your Customer Principles (805d4d5) — User_ or
  higher.

## Flow

1. Open the **Pre-Engagement > Client Acceptance > Management Integrity > Know Your
   Customer Principles** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The PMPJ sections shown on the form depend on the Money Laundring Issues worksheet of
  the same engagement.
