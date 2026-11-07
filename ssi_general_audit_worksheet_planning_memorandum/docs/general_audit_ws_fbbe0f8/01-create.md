# Create Audit Planning Memorandum - Details

> **Module:** `ssi_general_audit_worksheet_planning_memorandum`\
> **Model:** `general_audit_ws_fbbe0f8`\
> **Menu:** Risk Assessment > Audit Planning Memorandum > Audit Planning Memorandum -
> Details\
> **Actor:** user in group _Audit Planning Memorandum - Detail (fbbe0f8) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Audit Planning Memorandum - Detail (fbbe0f8) — User_ or
  higher.

## Flow

1. Open the **Risk Assessment > Audit Planning Memorandum > Audit Planning Memorandum -
   Details** menu. If **Audit Planning Memorandum** is not visible in the top menu bar,
   click the **+** button at its right end first. The menu list that opens shows **Audit
   Planning Memorandum** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
