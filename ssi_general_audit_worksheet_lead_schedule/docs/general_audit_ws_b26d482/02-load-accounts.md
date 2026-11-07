# Load Accounts - Worksheet

> **Module:** `ssi_general_audit_worksheet_lead_schedule`\
> **Model:** `general_audit_ws_b26d482`\
> **Menu:** Risk Responses > Result > Worksheet\
> **Actor:** user in group _Worksheet (b26d482) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The parent General Audit has at least one account.
- **Access:** User is in group _Worksheet (b26d482) — User_ or higher.

## Flow

1. Open the **Risk Responses > Result > Worksheet** menu. If **Result** is not visible
   in the top menu bar, click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Accounts** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every account of the General Audit that had none.
- Lines whose account is no longer in the General Audit are removed.
- Lines that already exist are kept as they are, so clicking **Accounts** again does not
  duplicate lines.
