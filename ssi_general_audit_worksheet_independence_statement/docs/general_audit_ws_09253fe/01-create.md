# Create Independence Statement

> **Module:** `ssi_general_audit_worksheet_independence_statement`\
> **Model:** `general_audit_ws_09253fe`\
> **Menu:** Pre-Engagement > Administrative > Independency Statement\
> **Actor:** user in group _Independence Statement (09253fe) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_09253fe` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Independence Statement (09253fe) — User_ or higher.

## Flow

1. Open the **Pre-Engagement > Administrative > Independency Statement** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Checklist** is empty until the checklist is populated on the open worksheet.
