# Populate Checklist — Audit Planning Memorandum

> **Module:** `ssi_general_audit_worksheet_planning_memorandum`\
> **Model:** `general_audit_ws_a753ab9`\
> **Menu:** Risk Assessment > Audit Planning Memorandum > Audit Planning Memorandum\
> **Actor:** user in group _Audit Planning Memorandum (a753ab9) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** Checklist master items for this worksheet exist (they are installed with
  the module).
- **Access:** User is in group _Audit Planning Memorandum (a753ab9) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Audit Planning Memorandum > Audit Planning Memorandum**
   menu. If **Audit Planning Memorandum** is not visible in the top menu bar, click the
   **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one row for every master checklist item; rows already
  present are kept, and rows whose master item no longer exists are removed.
- Clicking **Populate** again does not duplicate rows.
