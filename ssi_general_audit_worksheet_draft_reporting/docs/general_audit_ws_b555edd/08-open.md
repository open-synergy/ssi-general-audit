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
8. Open the **Statement of Changes in Equity** tab. **Reload** also fills this tab, one
   row per equity component, first for the current period and then for the previous
   period.
9. Optionally type the owner transactions on a row: **Issuance of Shares**, **Treasury
   Shares**, **Addition of Reserves** and **Dividends**, entered as the amount that
   changes the component (a dividend is negative).

## Post-Condition

- Status changes to **On Progress** (`open`).
- A document number is assigned to the worksheet (per the `sequence.template`
  configuration).
- **Statement of Financial Position** lists one row per standard account type of the
  General Audit that belongs to account groups T001-T008 (assets, liabilities and
  equity), each with its **Current Balance** and **Previous Balance**.
- **Statement of Comprehensive Income** lists the rows of account groups T009-T015
  (revenue, expenses and other comprehensive income) in the same way.
- **Statement of Changes in Equity** lists, per period, one row per equity component
  with **Opening Balance**, **Profit**, **OCI**, the four owner transactions, **Other
  Movement** and **Closing Balance**. Profit goes to Retained Earnings and OCI to Other
  Comprehensive Income. **Other Movement** is the part of the movement that profit, OCI
  and the typed-in owner transactions do not explain; it becomes 0 once the owner
  transactions are filled in. The previous period section has rows only when the General
  Audit keeps a previous period. The figures assume a trial balance before closing
  entries; when profit is already inside the Retained Earnings balance, that row shows
  the profit as **Other Movement**.
- Clicking **Reload** when owner transactions are typed in asks for confirmation first,
  because Reload clears them.
- Clicking **Reload** again does not duplicate rows; it removes the previous rows and
  creates them again from the General Audit. **Reload** is visible only while the
  worksheet is **Draft** or **On Progress**.
