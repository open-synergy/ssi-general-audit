# Create Specific Materiality

> **Module:** `ssi_general_audit_worksheet_preliminary_materiality`\
> **Model:** `general_audit_ws_6dcda0e`\
> **Menu:** Risk Assessment > Materiality > Specific Materiality\
> **Actor:** user in group _Specific Materiality — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** Fewer than two `general_audit_ws_6dcda0e` worksheets exist for that General
  Audit (at most two are allowed).
- **Access:** User is in group _Specific Materiality — User_ or higher.

## Flow

1. Open the **Risk Assessment > Materiality > Specific Materiality** menu. If
   **Materiality** is not visible in the top menu bar, click the **+** button at its
   right end first. The menu list that opens shows **Materiality** with its entries
   below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
