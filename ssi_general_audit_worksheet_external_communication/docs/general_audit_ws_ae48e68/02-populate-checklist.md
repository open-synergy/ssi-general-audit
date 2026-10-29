# Populate Checklist — External Communication

> **Module:** `ssi_general_audit_worksheet_external_communication`\
> **Model:** `general_audit_ws_ae48e68`\
> **Menu:** Risk Assessment > External Communication > External Communication\
> **Actor:** user in group _External Communication (ae48e68) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** Checklist master items for this worksheet exist (they are installed with
  the module).
- **Access:** User is in group _External Communication (ae48e68) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > External Communication > External Communication** menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one row for every master checklist item that applies; rows
  already present are kept, and rows whose master item no longer applies are removed.
- Clicking **Populate** again does not duplicate rows.
