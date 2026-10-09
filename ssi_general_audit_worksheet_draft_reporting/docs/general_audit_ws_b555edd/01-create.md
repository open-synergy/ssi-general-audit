# Create Report Formatting Control

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_b555edd`\
> **Menu:** Windup & Reporting > Draft Reporting > Report Formatting Control\
> **Actor:** user in group _Report Formatting Control (b555edd) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Report Formatting Control (b555edd) — User_ or higher.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Report Formatting Control** menu.
2. Click the **Create** button.
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Statement of Financial Position** and **Statement of Comprehensive Income** tabs
  are visible on the form, but both are still empty until **Reload** is clicked (see
  `08-open`).
