# Populate Auditor Expert Details

> **Module:** `ssi_general_audit_worksheet_expert`\
> **Model:** `general_audit_ws_bab9d32`\
> **Menu:** Risk Responses > Specific Procedures > Auditor Expert\
> **Actor:** user in group _Auditor Expert (bab9d32) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** At least one evaluation factor exists in the factor master of this
  worksheet.
- **Access:** User is in group _Auditor Expert (bab9d32) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Auditor Expert** menu. If
   **Specific Procedures** is not visible in the top menu bar, click the **+** button at
   its right end first.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every evaluation factor in the factor master; lines that
  already exist are kept with the explanation already entered.
- Lines whose factor is no longer in the factor master are removed.
- Clicking **Populate** again does not duplicate lines.
