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
- Existing lines are removed first and rebuilt, but the auditor's input is kept: the
  Planned Response flags and Assersion Types are stored on the account's standard
  detail, not on the line, so the rebuilt line shows them again.
- Inherent Risk and Fraud Impacted are re-synchronized from their source worksheets
  before the lines are rebuilt.
- Clicking **Detail** again does not duplicate lines.
