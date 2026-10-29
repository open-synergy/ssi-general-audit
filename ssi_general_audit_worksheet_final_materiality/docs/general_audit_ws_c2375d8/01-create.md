# Create Final Analytical Procedures

> **Module:** `ssi_general_audit_worksheet_final_materiality`\
> **Model:** `general_audit_ws_c2375d8`\
> **Menu:** Windup & Reporting > Final Analysis > Final Analytical Procedures > Final
> Analytical Procedures\
> **Actor:** user in group _Final Analytical Procedures — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_c2375d8` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Final Analytical Procedures — User_ or higher.

## Flow

1. Open the **Windup & Reporting > Final Analysis > Final Analytical Procedures > Final
   Analytical Procedures** menu. If **Final Analysis** is not visible in the top menu
   bar, click the **+** button at its right end first. The menu list that opens shows
   **Final Analysis** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
