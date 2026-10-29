# Populate Personnel — Competency, Availability and Independency Of Assignment Team

> **Module:** `ssi_general_audit_worksheet_acceptance_continuance`\
> **Model:** `general_audit_ws_b9d8a5c`\
> **Menu:** Pre-Engagement > Client Acceptance > Competency, Availability and
> Independency Of Assignment Team\
> **Actor:** user in group _Competency, Availability and Independency Of Assignment Team
> (b9d8a5c) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** At least one employee is flagged as available for audit assignments
  (**Audit** flag on the employee).
- **Access:** User is in group _Competency, Availability and Independency Of Assignment
  Team (b9d8a5c) — User_ (or higher).

## Flow

1. Open the **Pre-Engagement > Client Acceptance > Competency, Availability and
   Independency Of Assignment Team** menu.
2. Open the worksheet to work on.
3. Open the **List of KAP Personnel** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The personnel list has one row for every employee flagged for audit assignments, with
  the employee's job position; employees no longer flagged are removed from the list.
- Clicking **Populate** again does not duplicate rows.
