# Reload Links — Proposed Audit Opinion (fc75636)

> **Module:** ssi_general_audit_worksheet_review
>
> **Model:** `general_audit_ws_fc75636`
>
> **Menu:** Windup & Reporting > Final Report > Proposed Audit Opinion
>
> **Actor:** user in group _Independen Auditor Report (fc75636) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** none required — the Links tab fills in automatically as soon as the
  engagement has an Audit Final Memorandum (a8c54f3) worksheet whose status is **On
  Progress** or **Done**; the Reload button is only needed to pick up a sibling that
  appeared or changed status after this worksheet was opened.
- **Access:** User is in group _Independen Auditor Report (fc75636) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Final Report > Proposed Audit Opinion** menu.
2. Open the worksheet to view or refresh the Links tab for.
3. Open the **Links** tab.
4. Click the **Reload** button.

## Post-Condition

- The **Links** tab shows the **# Worksheet** field for Audit Final Memorandum and the
  **Proposed Audit Opinion** field — already filled in without needing step 4, whenever
  a matching Audit Final Memorandum worksheet (same General Audit, status On Progress or
  Done) exists.
- Clicking **Reload** re-runs the lookup, picking up a sibling that was created or
  changed status after this worksheet was opened.
- The **Checklist** tab and its rows are unaffected.
