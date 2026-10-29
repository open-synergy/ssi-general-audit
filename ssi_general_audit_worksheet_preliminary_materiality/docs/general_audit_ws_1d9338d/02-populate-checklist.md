# Populate Checklist — Preliminary Materiality

> **Module:** `ssi_general_audit_worksheet_preliminary_materiality`\
> **Model:** `general_audit_ws_1d9338d`\
> **Menu:** Risk Assessment > Materiality > Preliminary Materiality\
> **Actor:** user in group _Preliminary Materiality — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** The checklist item master (`general_audit_ws_1d9338d.item`) has items.
- **Access:** User is in group _Preliminary Materiality — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Materiality > Preliminary Materiality** menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one line for every checklist item; existing lines are kept
  and lines whose item no longer exists are removed.
- Clicking **Populate** again does not duplicate lines.
