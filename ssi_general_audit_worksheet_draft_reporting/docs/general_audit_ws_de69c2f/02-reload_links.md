# Reload Links — Final Discussion (de69c2f)

> **Module:** ssi_general_audit_worksheet_draft_reporting
>
> **Model:** `general_audit_ws_de69c2f`
>
> **Menu:** Windup & Reporting > Draft Reporting > Final Discussion
>
> **Actor:** user in group _Final Discussion (de69c2f) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** none required — the Links tab fills in automatically as soon as the
  engagement has an Audit Result (ff42fdc), Management Letter (ae598e6), or Management
  Representation (bbbdfe7) worksheet whose status is **On Progress** or **Done**; the
  Reload button is only needed to pick up a sibling that appeared or changed status
  after this worksheet was opened.
- **Access:** User is in group _Final Discussion (de69c2f) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Final Discussion** menu.
2. Open the worksheet to view or refresh the Links tab for.
3. Open the **Links** tab.
4. Click the **Reload** button.

## Post-Condition

- The **Links** tab shows, for each of Audit Result, Management Letter, and Management
  Representation: the **# Worksheet** document number, its **State**, and its
  **Conclusion** — already filled in without needing step 4, whenever a matching sibling
  worksheet (same General Audit, status On Progress or Done) exists.
- Clicking **Reload** re-runs the lookup for all three references at once, picking up
  any sibling that was created or changed status after this worksheet was opened.
- The **Checklist** tab and its rows are unaffected.
