# Create Analytical Procedures – Cycle

> **Module:** `ssi_general_audit_worksheet_analytic_cycle`\
> **Model:** `general_audit_ws_a3c9d2e`\
> **Menu:** Risk Responses > Substantive Test > Analytical Procedures – Cycle\
> **Actor:** user in group _Analytical Procedures – Cycle (a3c9d2e) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Analytical Procedures – Cycle (a3c9d2e) — User_ or
  higher.

## Flow

1. Open the **Risk Responses > Substantive Test > Analytical Procedures – Cycle** menu.
   If **Substantive Test** is not visible in the top menu bar, click the **+** button at
   its right end first. The menu list that opens shows **Substantive Test** with its
   entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
