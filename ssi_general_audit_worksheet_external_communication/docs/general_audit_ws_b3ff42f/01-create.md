# Create Communication With Management

> **Module:** `ssi_general_audit_worksheet_external_communication`\
> **Model:** `general_audit_ws_b3ff42f`\
> **Menu:** Risk Assessment > External Communication > Communication With Management\
> **Actor:** user in group _Communication With Management (b3ff42f) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_b3ff42f` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Communication With Management (b3ff42f) — User_ or
  higher.

## Flow

1. Open the **Risk Assessment > External Communication > Communication With Management**
   menu. If **External Communication** is not visible in the top menu bar, click the
   **+** button at its right end first. The menu list that opens shows **External
   Communication** with its entry below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Checklist** is empty until **Populate** is clicked on the open worksheet (see
  `02-populate-checklist`).
