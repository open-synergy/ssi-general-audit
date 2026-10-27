# Populate Details — Audit Evidence Evaluation Detail (cae598e)

> **Module:** `ssi_general_audit_worksheet_review`
>
> **Model:** `general_audit_ws_cae598e`
>
> **Menu:** Windup & Reporting > Review > Audit Evidence > Audit Evidence
> Evaluation-Detail
>
> **Actor:** user in group _Audit Evidence Evaluation Detail (cae598e) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** An **Audit Quality** worksheet of the same **General Audit** already has
  detail rows. Populate it first, see `01-populate` of the Audit Quality worksheet.
- **Access:** User is in group _Audit Evidence Evaluation Detail (cae598e) — User_ (or
  higher).

## Flow

1. Open the **Windup & Reporting > Review > Audit Evidence > Audit Evidence
   Evaluation-Detail** menu.
2. Open the worksheet to prepare.
3. Open the **Details** tab.
4. Click **Populate**.

## Post-Condition

- The **Details** tab holds one evaluation row for every Audit Quality detail row of the
  same General Audit.
- Existing rows are kept, with the evaluation already entered on them.
- Rows whose Audit Quality detail row no longer exists are removed.
