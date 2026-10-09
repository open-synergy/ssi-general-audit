# Open Report Formatting Control

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_b555edd`\
> **Menu:** Windup & Reporting > Draft Reporting > Report Formatting Control\
> **Actor:** the worksheet's assigned user/reviewer, the linked General Audit's user/reviewer,
> a System Administrator, or a member of group _Report Formatting Control (b555edd) — Validator_\
> **State:** `draft` → `open`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_reload_account` (Reload)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `draft` to the actor.
- **Config:** An active `sequence.template` exists for this model (the document number
  is assigned when the worksheet is started).
- **Data:** The linked General Audit has standard account type lines, so Reload has
  something to show.
- **Access:** User matches one of the personas listed under **Actor**.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Report Formatting Control** menu.
2. Open the record to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Statement of Financial Position** tab.
6. Click the **Reload** button to fill both statement tabs from the General Audit's
   standard account type lines.
7. Open the **Statement of Comprehensive Income** tab to review its lines.

## Post-Condition

- Status changes to **On Progress** (`open`).
- A document number is assigned to the worksheet (per the `sequence.template`
  configuration).
- **Statement of Financial Position** lists one row per standard account type of the
  General Audit that belongs to account groups T001-T008 (assets, liabilities and
  equity), each with its **Current Balance** and **Previous Balance**.
- **Statement of Comprehensive Income** lists the rows of account groups T009-T015
  (revenue, expenses and other comprehensive income) in the same way.
- Clicking **Reload** again does not duplicate rows; it removes the previous rows and
  creates them again from the General Audit. **Reload** is visible only while the
  worksheet is **Draft** or **On Progress**.
