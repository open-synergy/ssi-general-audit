# Populate Details — Audit Quality (bcc0d76)

> **Module:** `ssi_general_audit_worksheet_review`
>
> **Model:** `general_audit_ws_bcc0d76`
>
> **Menu:** Windup & Reporting > Review > Audit Quality
>
> **Actor:** user in group _Audit Quality (bcc0d76) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** The same **General Audit** already has worksheets whose worksheet type is
  marked as a main worksheet. Types without such a worksheet produce no row.
- **Access:** User is in group _Audit Quality (bcc0d76) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Review > Audit Quality** menu.
2. Open the worksheet to prepare.
3. Open the **Details** tab.
4. Click **Populate**.

## Post-Condition

- The **Details** tab holds one row per main worksheet type of the same General Audit.
  When a type has several worksheets, only one of them is listed.
- Existing rows are kept. **Populate** does not create duplicates.
- Rows whose source worksheet no longer qualifies are removed, except rows already used
  by an Audit Evidence Evaluation worksheet. Those stay untouched.
