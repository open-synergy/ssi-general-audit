# Create Fraud Factor Analysis

> **Module:** `ssi_general_audit_worksheet_understanding_entity`\
> **Model:** `general_audit_ws_c0e0eec`\
> **Menu:** Risk Assessment > Understanding The Entity > Fraud Factor Analysis\
> **Actor:** user in group _Fraud Factor Analysis (c0e0eec) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_c0e0eec` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Fraud Factor Analysis (c0e0eec) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Understanding The Entity > Fraud Factor Analysis** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Details** tab is empty until the **Procedures** button is used (see
  `02-populate-procedures.md`).
