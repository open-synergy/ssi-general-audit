# Load Details — Account Level Inherent Risk

> **Module:** `ssi_general_audit_worksheet_inherent_risk`\
> **Model:** `general_audit_ws_a418d89`\
> **Menu:** Risk Assessment > Inherent Risk > Inherent Risk - Account Level\
> **Actor:** user in group _Account Level Inherent Risks (a418d89) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The linked General Audit has at least one standard detail (account or
  disclosure area).
- **Access:** User is in group _Account Level Inherent Risks (a418d89) — User_ or
  higher.

## Flow

1. Open the **Risk Assessment > Inherent Risk > Inherent Risk - Account Level** menu. If
   **Inherent Risk** is not visible in the top menu bar, click the **+** button at its
   right end first.
2. Open the worksheet to work on.
3. Open the **Inherent Risks** tab.
4. Click the **Details** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every standard detail of the General Audit; lines that
  already exist are kept with the assessment already entered.
- Lines whose standard detail is no longer part of the General Audit are removed.
- Clicking **Details** again does not duplicate lines.
