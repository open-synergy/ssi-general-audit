# Create Account Level ROMM

> **Module:** `ssi_general_audit_worksheet_romm`\
> **Model:** `general_audit_ws_d66d87a`\
> **Menu:** Risk Assessment > ROMM > ROMM - Account Level\
> **Actor:** user in group _Account Level ROMM (d66d87a) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_d66d87a` worksheet exists yet for that General Audit.
- **Access:** User is in group _Account Level ROMM (d66d87a) — User_ or higher.

## Flow

1. Open the **Risk Assessment > ROMM > ROMM - Account Level** menu. If **ROMM** is not
   visible in the top menu bar, click the **+** button at its right end first. The menu
   list that opens shows **ROMM** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
