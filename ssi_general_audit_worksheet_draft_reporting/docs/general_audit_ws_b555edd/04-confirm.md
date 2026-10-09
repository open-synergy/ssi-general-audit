# Confirm Report Formatting Control

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_b555edd`\
> **Menu:** Windup & Reporting > Draft Reporting > Report Formatting Control\
> **Actor:** the worksheet's assigned user/reviewer, the linked General Audit's user/reviewer,
> a System Administrator, or a member of group _Report Formatting Control (b555edd) — Validator_\
> **State:** `open` → `confirm`\
> **Requires:** `08-open`

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Record:** **Conclusion** and its notes field are filled (not required before
  confirming, but normally filled in first).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `open` to the actor.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver.
- **Access:** User matches one of the personas listed under **Actor**.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Report Formatting Control** menu.
2. Open the record to confirm.
3. If not already filled, fill in **Conclusion** and its notes field on the
   **Conclusion** group.
4. Click the **Confirm** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval** (`confirm`).
- Approval records are created for each approver defined by the approval template.
- The **Statement of Financial Position** and **Statement of Comprehensive Income** tabs
  keep the rows loaded by **Reload**.
