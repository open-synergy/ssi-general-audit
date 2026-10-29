# Populate Checklist — Team Communication Pre-Engagement

> **Module:** `ssi_general_audit_worksheet_team_communication`\
> **Model:** `general_audit_ws_437fc8f`\
> **Menu:** Pre-Engagement > Team Communication > Team Communication\
> **Actor:** user in group _Team Communitation - Pre-Engagement (437fc8f) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** Checklist master items for this worksheet exist (they are installed with
  the module).
- **Access:** User is in group _Team Communitation - Pre-Engagement (437fc8f) — User_
  (or higher).

## Flow

1. Open the **Pre-Engagement > Team Communication > Team Communication** menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one row for every master checklist item that applies; rows
  already present are kept, and rows whose master item no longer applies are removed.
- Clicking **Populate** again does not duplicate rows.
