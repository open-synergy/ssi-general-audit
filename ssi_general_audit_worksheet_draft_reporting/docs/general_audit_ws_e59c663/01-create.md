# Create Draft Financial Statements

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_e59c663`\
> **Menu:** Windup & Reporting > Draft Reporting > Draft Financial Statements\
> **Actor:** user in group _Draft Financial Statements (e59c663) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Access:** User is in group _Draft Financial Statements (e59c663) — User_ or higher.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Draft Financial Statements** menu.
2. Click the **Create** button.
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Review Procedure Checklist** tab (WR.160 review procedure checklist, shown
  first) and the **Completeness of financial statements cheklist** tab (WR.160.1
  completeness checklist, shown second) are both visible on the form, but both are still
  empty — they are only populated after the worksheet is opened (see `08-open`).
