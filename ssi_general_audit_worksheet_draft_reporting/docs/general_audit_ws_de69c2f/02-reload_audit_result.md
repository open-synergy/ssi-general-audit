# Reload Audit Result — Final Discussion (de69c2f)

> **Module:** ssi_general_audit_worksheet_draft_reporting
>
> **Model:** `general_audit_ws_de69c2f`
>
> **Menu:** Windup & Reporting > Draft Reporting > Final Discussion
>
> **Actor:** user in group _Final Discussion (de69c2f) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** none required — the reload works whether or not the engagement already has
  an Audit Result (ff42fdc) worksheet.
- **Access:** User is in group _Final Discussion (de69c2f) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Final Discussion** menu.
2. Open the worksheet to reload the Audit Result reference for.
3. Open the **Audit Result** tab.
4. Click the **Reload** button.

## Post-Condition

- The **# Audit Result** field shows the document number of the
  `general_audit_ws_ff42fdc` worksheet that belongs to the same General Audit, if one
  exists.
- If no such worksheet exists yet, the field stays/becomes empty; no error is shown.
- The **Checklist**, **Management Letter**, and **Management Representation** tabs and
  their fields are unaffected.
