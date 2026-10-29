# Populate Checklist — Communication With Previous Auditor

> **Module:** `ssi_general_audit_worksheet_acceptance_continuance`\
> **Model:** `general_audit_ws_0427d28`\
> **Menu:** Pre-Engagement > Client Acceptance > Communication With Previous Auditor\
> **Actor:** user in group _Communication With Previous Auditor (0427d28) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The engagement is an **Initial Engagement** (the firm has not audited the
  client for 2 or more consecutive years) and the prior period financial statement is
  audited; otherwise the **Checklist** tab is hidden.
- **Config:** Checklist master items for this worksheet exist (they are installed with
  the module).
- **Access:** User is in group _Communication With Previous Auditor (0427d28) — User_
  (or higher).

## Flow

1. Open the **Pre-Engagement > Client Acceptance > Communication With Previous Auditor**
   menu.
2. Open the worksheet to work on.
3. Open the **Checklist** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Checklist** tab has one row for every master checklist item that applies; rows
  already present are kept, and rows whose master item no longer applies are removed.
- Clicking **Populate** again does not duplicate rows.
