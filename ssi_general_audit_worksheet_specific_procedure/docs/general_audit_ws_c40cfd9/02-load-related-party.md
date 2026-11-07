# Load Related Parties - Related Party Transaction

> **Module:** `ssi_general_audit_worksheet_specific_procedure`\
> **Model:** `general_audit_ws_c40cfd9`\
> **Menu:** Risk Responses > Specific Procedures > Related Party Transaction\
> **Actor:** user in group _Related Party Transaction (c40cfd9) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **Understanding of the Entity Worksheet** field on the **Related
  Parties** tab is filled with a worksheet of the same General Audit, and that worksheet
  has related parties.
- **Access:** User is in group _Related Party Transaction (c40cfd9) — User_ or higher.

## Flow

1. Open the **Risk Responses > Specific Procedures > Related Party Transaction** menu.
   If **Specific Procedures** is not visible in the top menu bar, click the **+** button
   at its right end first.
2. Open the worksheet to work on.
3. Open the **Related Parties** tab.
4. Click the **Related Parties** button. The button is only visible while the status is
   **On Progress**.

## Post-Condition

- The **Related Parties** list has one line for every related party of the selected
  Understanding of the Entity worksheet.
- The relation and related account types of each party are copied into both the initial
  and the final columns.
- Existing lines are removed first and rebuilt, so any input already entered on them is
  lost.
- Clicking the button again does not duplicate lines.
