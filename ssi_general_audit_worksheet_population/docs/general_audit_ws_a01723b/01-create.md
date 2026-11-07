# Create Population

> **Module:** `ssi_general_audit_worksheet_population`\
> **Model:** `general_audit_ws_a01723b`\
> **Menu:** Risk Responses > General Procedures > Populations\
> **Actor:** user in group _Population (a01723b) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** At least one **Population Type** exists.
- **Access:** User is in group _Population (a01723b) — User_ or higher.

## Flow

1. Open the **Risk Responses > General Procedures > Populations** menu. If **General
   Procedures** is not visible in the top menu bar, click the **+** button at its right
   end first. The menu list that opens shows **General Procedures** with its entries
   below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required fields:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
   - **Population Type**: select the type of the population. It is on the **Raw Data**
     tab.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
