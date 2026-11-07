# Load Confirmation Procedures - Related Party Transaction

> **Module:** `ssi_general_audit_worksheet_specific_procedure`\
> **Model:** `general_audit_ws_c40cfd9`\
> **Menu:** Risk Responses > Specific Procedures > Related Party Transaction\
> **Actor:** user in group _Related Party Transaction (c40cfd9) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** At least one confirmation procedure exists in the related party confirmation
  procedure master.
- **Access:** User is in group _Related Party Transaction (c40cfd9) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Related Party Transaction** menu.
   If **Specific Procedures** is not visible in the top menu bar, click the **+** button
   at its right end first.
2. Open the worksheet to work on.
3. Open the **Confirmation Procedures** tab.
4. Click the **Confirmation Procedures** button. The button is only visible while the
   status is **On Progress**.

## Post-Condition

- The tab has one line for every confirmation procedure in the master; lines that
  already exist are kept with the input already entered.
- Lines whose procedure is no longer in the master are removed.
- Clicking the button again does not duplicate lines.
