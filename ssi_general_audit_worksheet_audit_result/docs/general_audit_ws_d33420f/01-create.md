# Create Control Deficiencies

> **Module:** `ssi_general_audit_worksheet_audit_result`\
> **Model:** `general_audit_ws_d33420f`\
> **Menu:** Windup & Reporting > Audit Result > Audit Result Formulation > Control
> Deficiencies\
> **Actor:** user in group _Control Deficiencies (d33420f) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_d33420f` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Control Deficiencies (d33420f) — User_ or higher.

## Flow

1. Open the **Windup & Reporting > Audit Result > Audit Result Formulation > Control
   Deficiencies** menu. If **Audit Result** is not visible in the top menu bar, click
   the **+** button at its right end first. The menu list that opens shows **Audit
   Result** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Details** tab is empty; lines are added while the worksheet is **On Progress**.
