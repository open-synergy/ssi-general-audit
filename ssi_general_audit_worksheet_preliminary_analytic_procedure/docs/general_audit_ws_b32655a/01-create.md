# Create Vertical and Horizontal Analysis

> **Module:** `ssi_general_audit_worksheet_preliminary_analytic_procedure`\
> **Model:** `general_audit_ws_b32655a`\
> **Menu:** Risk Assessment > Analytical Procedures > Analytic Procedures - Vertical and
> Horizontal Analysis\
> **Actor:** user in group _Preliminary Analytic Procedure - Vertical and Horizontal Analysis
> — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** Fewer than two `general_audit_ws_b32655a` worksheets exist for that General
  Audit (at most two are allowed, one per **Balance Type**).
- **Access:** User is in group _Preliminary Analytic Procedure - Vertical and Horizontal
  Analysis — User_ or higher.

## Flow

1. Open the **Risk Assessment > Analytical Procedures > Analytic Procedures - Vertical
   and Horizontal Analysis** menu. If **Analytical Procedures** is not visible in the
   top menu bar, click the **+** button at its right end first. The menu list that opens
   shows **Analytical Procedures** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Analysis** tab lines are loaded only after **Reload** is clicked on the open
  worksheet (see `02-reload-analysis`).
