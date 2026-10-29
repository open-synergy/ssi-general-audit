# Create Preliminary Materiality

> **Module:** `ssi_general_audit_worksheet_preliminary_materiality`\
> **Model:** `general_audit_ws_1d9338d`\
> **Menu:** Risk Assessment > Materiality > Preliminary Materiality\
> **Actor:** user in group _Preliminary Materiality — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_1d9338d` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Preliminary Materiality — User_ or higher.

## Flow

1. Open the **Risk Assessment > Materiality > Preliminary Materiality** menu. If
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
