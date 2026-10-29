# Create Understanding of preparation of Financial Statements

> **Module:** `ssi_general_audit_worksheet_understanding_entity`\
> **Model:** `general_audit_ws_f6a227`\
> **Menu:** Risk Assessment > Understanding The Entity > Understanding of preparation of
> Financial Statements\
> **Actor:** user in group _Understanding of preparation of Financial Statements (f6a227)
> — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_f6a227` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Understanding of preparation of Financial Statements
  (f6a227) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Understanding The Entity > Understanding of preparation
   of Financial Statements** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Details** tab is empty.
