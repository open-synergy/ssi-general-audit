# Load Computation - Going Concern

> **Module:** `ssi_general_audit_worksheet_specific_procedure`\
> **Model:** `general_audit_ws_fbf57ee`\
> **Menu:** Risk Responses > Specific Procedures > Going Concern\
> **Actor:** user in group _Going Concern Analysis (fbf57ee) — User_

## Pre-Condition

- **Record:** Status is **Draft** (`draft`) or **On Progress** (`open`).
- **Data:** The linked General Audit has computation lines whose computation item is
  flagged for going concern analysis.
- **Config:** Optional: a **Z-Score Coefficient Set** is selected on the tab. Without it
  every coefficient is zero.
- **Access:** User is in group _Going Concern Analysis (fbf57ee) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Going Concern** menu. If **Specific
   Procedures** is not visible in the top menu bar, click the **+** button at its right
   end first.
2. Open the worksheet to work on.
3. Open the **Computation** tab.
4. Click the **Computation** button. The button is only visible while the status is
   **Draft** or **On Progress**.

## Post-Condition

- The **Computation** list is synchronised with the going-concern computation lines of
  the General Audit. A line is added for each computation that has none, and the line of
  a computation that no longer qualifies is removed.
- The coefficient of a new line comes from the selected **Z-Score Coefficient Set**.
  Kept lines are not rewritten, so a coefficient changed before is not lost.
- The **Current Amount** and **Result** of the kept lines are refreshed from the current
  trial balance.
- Clicking the button again does not duplicate lines.
