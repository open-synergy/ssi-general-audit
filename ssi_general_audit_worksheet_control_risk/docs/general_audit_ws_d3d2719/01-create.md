# Create General Control Evaluation

> **Module:** `ssi_general_audit_worksheet_control_risk`\
> **Model:** `general_audit_ws_d3d2719`\
> **Menu:** Risk Assessment > Control Risk > Control Risk - Entity Level > General
> Control Evaluations\
> **Actor:** user in group _General Control Evaluation (d3d2719) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_d3d2719` worksheet exists yet for that General Audit.
- **Access:** User is in group _General Control Evaluation (d3d2719) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Control Risk > Control Risk - Entity Level > General
   Control Evaluations** menu. If **Control Risk** is not visible in the top menu bar,
   click the **+** button at its right end first. The menu list that opens shows
   **Control Risk** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
