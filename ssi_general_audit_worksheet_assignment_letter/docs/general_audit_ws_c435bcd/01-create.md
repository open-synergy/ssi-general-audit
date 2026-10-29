# Create Assignment Letter

> **Module:** `ssi_general_audit_worksheet_assignment_letter`\
> **Model:** `general_audit_ws_c435bcd`\
> **Menu:** Pre-Engagement > Administrative > Assignment Letter\
> **Actor:** user in group _Assignment Letter (c435bcd) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_c435bcd` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Assignment Letter (c435bcd) — User_ or higher.

## Flow

1. Open the **Pre-Engagement > Administrative > Assignment Letter** menu.
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
