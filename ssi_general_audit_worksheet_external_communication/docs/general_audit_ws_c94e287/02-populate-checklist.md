# Populate Checklist — Communication With TCWG

> **Module:** `ssi_general_audit_worksheet_external_communication`\
> **Model:** `general_audit_ws_c94e287`\
> **Menu:** Risk Assessment > External Communication > Communication With TCWG\
> **Actor:** user in group _Communication With TCWG (c94e287) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** Checklist master items for this worksheet exist (they are installed with
  the module).
- **Access:** User is in group _Communication With TCWG (c94e287) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > External Communication > Communication With TCWG** menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one row for every master checklist item that applies; rows
  already present are kept, and rows whose master item no longer applies are removed.
- Clicking **Populate** again does not duplicate rows.
