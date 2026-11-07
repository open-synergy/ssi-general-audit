# Load Analysis - Going Concern

> **Module:** `ssi_general_audit_worksheet_specific_procedure`\
> **Model:** `general_audit_ws_fbf57ee`\
> **Menu:** Risk Responses > Specific Procedures > Going Concern\
> **Actor:** user in group _Going Concern Analysis (fbf57ee) — User_

## Pre-Condition

- **Record:** Status is **Draft** (`draft`) or **On Progress** (`open`).
- **Data:** At least one going concern indicator exists in the going concern master.
- **Access:** User is in group _Going Concern Analysis (fbf57ee) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Going Concern** menu. If **Specific
   Procedures** is not visible in the top menu bar, click the **+** button at its right
   end first.
2. Open the worksheet to work on.
3. Open the **Analysis** tab.
4. Click the **Analysis** button. The button is only visible while the status is
   **Draft** or **On Progress**.

## Post-Condition

- The tab has one line for every going concern indicator in the master; lines that
  already exist are kept with the input already entered.
- Lines whose indicator is no longer in the master are removed.
- Clicking the button again does not duplicate lines.
