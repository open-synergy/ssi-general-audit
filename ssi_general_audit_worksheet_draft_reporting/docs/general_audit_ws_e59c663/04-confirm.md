# Confirm Draft Financial Statements

> **Module:** `ssi_general_audit_worksheet_draft_reporting`\
> **Model:** `general_audit_ws_e59c663`\
> **Menu:** Windup & Reporting > Draft Reporting > Draft Financial Statements\
> **Actor:** the worksheet's assigned user/reviewer, the linked General Audit's user/reviewer,
> a System Administrator, or a member of group _Draft Financial Statements (e59c663) — Validator_\
> **State:** `open` → `confirm`\
> **Requires:** `08-open`

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `open` to the actor.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver.
- **Access:** User matches one of the personas listed under **Actor**.

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Draft Financial Statements** menu.
2. Open the record to confirm.
3. On the **Conclusion** group, fill in **Conclusion** and the notes field, if not
   already filled.
4. Click the **Confirm** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval** (`confirm`).
- Approval records are created for each approver defined by the approval template.
- The **Checklist** tab (WR.160.1) and the **Review Procedure Checklist** tab (WR.160),
  along with their answers, remain as entered; confirming does not require every
  checklist row on either tab to be answered.
