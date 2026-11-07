# Load Detail - Account Level ROMM

> **Module:** `ssi_general_audit_worksheet_romm`\
> **Model:** `general_audit_ws_d66d87a`\
> **Menu:** Risk Assessment > ROMM > ROMM - Account Level\
> **Actor:** user in group _Account Level ROMM (d66d87a) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The linked General Audit has at least one standard detail (account or
  disclosure area).
- **Access:** User is in group _Account Level ROMM (d66d87a) — User_ or higher.

## Flow

1. Open the **Risk Assessment > ROMM > ROMM - Account Level** menu. If **ROMM** is not
   visible in the top menu bar, click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Detail** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every standard detail of the General Audit.
- Existing lines are removed first and rebuilt, so any input already entered on them is
  lost.
- Clicking **Detail** again does not duplicate lines.
