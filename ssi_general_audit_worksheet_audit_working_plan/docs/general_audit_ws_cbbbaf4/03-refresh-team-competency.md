# Refresh Team Competency — Audit Working Plan

> **Module:** `ssi_general_audit_worksheet_audit_working_plan`\
> **Model:** `general_audit_ws_cbbbaf4`\
> **Menu:** Pre-Engagement > Audit Working Plan > Audit Working Plan\
> **Actor:** user in group _Audit Working Plan (cbbbaf4) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **Links** tab has a worksheet selected under **Competency**, and that
  worksheet has at least one personnel row with **Select As Team** set to **Yes**.
- **Access:** User is in group _Audit Working Plan (cbbbaf4) — User_ (or higher).

## Flow

1. Open the **Pre-Engagement > Audit Working Plan > Audit Working Plan** menu.
2. Open the worksheet to work on.
3. Open the **Team Competency Analysis** tab.
4. Click the **Refresh** button. The button is only visible when the status is not
   **Draft**.

## Post-Condition

- The **Team Competency Analysis** tab has one row for every personnel row selected as
  team in the linked Competency worksheet, with the competency upgrades still needed by
  that member.
- Rows of members who are no longer selected are removed.
