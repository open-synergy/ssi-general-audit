# Load Procedures - Key Audit Procedures

> **Module:** `ssi_general_audit_worksheet_lead_schedule`\
> **Model:** `general_audit_ws_e51bb1c`\
> **Menu:** Risk Responses > Substantive Test > Key Audit Procedures\
> **Actor:** user in group _Key Audit Procedures (e51bb1c) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **Standard Account** field is filled, and procedure categories exist for
  that account type.
- **Access:** User is in group _Key Audit Procedures (e51bb1c) — User_ or higher.

## Flow

1. Open the **Risk Responses > Substantive Test > Key Audit Procedures** menu. If
   **Substantive Test** is not visible in the top menu bar, click the **+** button at
   its right end first.
2. Open the worksheet to work on.
3. Open the **Detail** tab.
4. Click the **Procedures** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every procedure category of the selected account type, with
  its assertion types and steps.
- Existing lines are removed first and rebuilt, so any input already entered on them is
  lost.
- Clicking **Procedures** again does not duplicate lines.
