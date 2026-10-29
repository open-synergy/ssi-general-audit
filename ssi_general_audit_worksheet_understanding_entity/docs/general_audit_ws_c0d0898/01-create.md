# Create Going Concern Analysis

> **Module:** `ssi_general_audit_worksheet_understanding_entity`\
> **Model:** `general_audit_ws_c0d0898`\
> **Menu:** Risk Assessment > Understanding The Entity > Going Concern Analysis\
> **Actor:** user in group _Going concern analysis (c0d0898) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_c0d0898` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Going concern analysis (c0d0898) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Understanding The Entity > Going Concern Analysis**
   menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Details** tab is filled with the going concern items when the worksheet is
  opened.
