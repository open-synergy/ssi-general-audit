# Create Audit Working Plan

> **Module:** `ssi_general_audit_worksheet_audit_working_plan`\
> **Model:** `general_audit_ws_cbbbaf4`\
> **Menu:** Pre-Engagement > Audit Working Plan > Audit Working Plan\
> **Actor:** user in group _Audit Working Plan (cbbbaf4) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_cbbbaf4` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Audit Working Plan (cbbbaf4) — User_ or higher.

## Flow

1. Open the **Pre-Engagement > Audit Working Plan > Audit Working Plan** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**. The **Links** tab is also pre-filled with the Client Acceptance
   and Competency worksheets of the same General Audit, when they exist.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Team Allocations** and **Team Competency Analysis** tabs are empty until the
  worksheet is opened.
