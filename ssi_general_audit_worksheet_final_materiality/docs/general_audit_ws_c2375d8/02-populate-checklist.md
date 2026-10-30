# Populate Checklist — Final Analytical Procedures

> **Module:** `ssi_general_audit_worksheet_final_materiality`\
> **Model:** `general_audit_ws_c2375d8`\
> **Menu:** Windup & Reporting > Final Analysis > Final Analytical Procedures > Final
> Analytical Procedures\
> **Actor:** user in group _Final Analytical Procedures — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** The checklist item master (`general_audit_ws_c2375d8.item`) has items.
- **Access:** User is in group _Final Analytical Procedures — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Final Analysis > Final Analytical Procedures > Final
   Analytical Procedures** menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one line for every checklist item; existing lines are kept
  and lines whose item no longer exists are removed.
- Clicking **Populate** again does not duplicate lines.
