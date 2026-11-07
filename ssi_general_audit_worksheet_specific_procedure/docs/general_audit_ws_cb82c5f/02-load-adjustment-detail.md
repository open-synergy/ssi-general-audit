# Load Adjustment Details - Subsequent Event

> **Module:** `ssi_general_audit_worksheet_specific_procedure`\
> **Model:** `general_audit_ws_cb82c5f`\
> **Menu:** Risk Responses > Specific Procedures > Subsequent Event\
> **Actor:** user in group _Subsequent Event (cb82c5f) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** At least one subsequent event that needs adjustment exists in the subsequent
  event master.
- **Access:** User is in group _Subsequent Event (cb82c5f) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Subsequent Event** menu. If
   **Specific Procedures** is not visible in the top menu bar, click the **+** button at
   its right end first.
2. Open the worksheet to work on.
3. Open the **Subsequent Events** tab.
4. In the **Need Adjustment** section, the first of the two sections on the tab, locate
   the button. Both sections use the same **Detail** label; this one sits above the
   **Need Adjustment** list.
5. Click the **Detail** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Need Adjustment** list has one line for every subsequent event in the master
  that needs adjustment; lines that already exist are kept with the input already
  entered.
- Lines whose event is no longer in the master are removed.
- Clicking the button again does not duplicate lines.
