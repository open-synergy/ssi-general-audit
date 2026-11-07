# Generate Closing - Worksheet

> **Module:** `ssi_general_audit_worksheet_lead_schedule`\
> **Model:** `general_audit_ws_b26d482`\
> **Menu:** Risk Responses > Result > Worksheet\
> **Actor:** user in group _Worksheet (b26d482) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **Closing Type** field of the parent General Audit is filled.
- **Access:** User is in group _Worksheet (b26d482) — User_ or higher.

## Flow

1. Open the **Risk Responses > Result > Worksheet** menu. If **Result** is not visible
   in the top menu bar, click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Closing** tab.
4. Click the **Generate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The closing lines of the General Audit are regenerated for the current and the
  previous period, and shown on the **Closing** tab.
- Closing lines that existed before are replaced.
- Without a Closing Type the system shows an error and changes nothing.
