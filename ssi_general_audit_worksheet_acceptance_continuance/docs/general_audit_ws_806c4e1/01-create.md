# Create Acceptance and Continuance of Client Relationships Analysis

> **Module:** `ssi_general_audit_worksheet_acceptance_continuance`\
> **Model:** `general_audit_ws_806c4e1`\
> **Menu:** Pre-Engagement > Client Acceptance > Acceptance and Continuance of Client
> Relationships Analysis\
> **Actor:** user in group _Acceptance and Continuance of Client Relationships Analysis (806c4e1)
> — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_806c4e1` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Acceptance and Continuance of Client Relationships
  Analysis (806c4e1) — User_ or higher.

## Flow

1. Open the **Pre-Engagement > Client Acceptance > Acceptance and Continuance of Client
   Relationships Analysis** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Risk** and **Client Relationship** fields are empty; they are set while the
  worksheet is worked on.
