# Reload Posture — Audit Result (ff42fdc)

> **Module:** `ssi_general_audit_worksheet_draft_reporting`
>
> **Model:** `general_audit_ws_ff42fdc`
>
> **Menu:** Windup & Reporting > Draft Reporting > Final Discussion > Audit Result
>
> **Actor:** user in group _Audit Result (ff42fdc) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** The related General Audit has one or more `general_audit.detail` lines
  (accounts registered on the engagement through the account mapping / reload flow),
  each linked to a `client_account` whose type is assigned to a `client_account_group`.
- **Access:** User is in group _Audit Result (ff42fdc) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Draft Reporting > Final Discussion > Audit Result**
   menu.
2. Open the worksheet to load the posture for.
3. Open the **Posture Report** tab (the first tab).
4. Click the **Reload** button.

## Post-Condition

- The **Posture Report** table is (re)built with:
  - One **Account Group** row per `client_account_group` that has accounts registered on
    the General Audit, each showing Unaudited, Adjustment (Debit), Adjustment (Credit),
    Audited, and **Previous** amounts aggregated from the account detail lines belonging
    to that group. **Previous** sums the previous-period balance of the same accounts.
    When the General Audit has a KKA Worksheet (the newest one that is not cancelled or
    rejected), **Audited** is read from it: the Balance Sheet column for asset,
    liability and equity groups (plus the closing of a type that no account receives),
    the Current Profit column for profit and loss groups and the OCI column for other
    comprehensive income groups. Without a KKA Worksheet, **Audited** sums the audited
    balance of the account detail lines and adds the closing amount that lands in the
    group. Press **Reload** after the KKA Worksheet or the closing lines change.
  - Nine fixed **Total** rows (Total Asset, Total Liability, Total Equity, Total
    Liability and Equity, Gross Profit, Operating Profit, Profit Before Tax, Profit
    After Tax, Comprehensive Income), interleaved right after their component Account
    Group rows and shown in **bold**. Total rows always appear, even when their
    component account groups have no data.
  - With a KKA Worksheet, the **Audited** column of Profit After Tax is its Total
    Current Profit and that of Comprehensive Income is Total Current Profit plus Total
    OCI.
  - A Total row shows the plain sums of the debit and credit adjustments of its
    component account groups. The Adjustment (Debit) and Adjustment (Credit) columns are
    blank on the profit and loss subtotals (Gross Profit, Operating Profit, Profit
    Before Tax, Profit After Tax, Comprehensive Income); this is set per row with **Show
    Adjustment** in **Posture Report Layout**.
  - The rows follow the order set in **Posture Report Layout** (Configuration menu); an
    account group that is not listed there is shown after all listed rows.
- An Account Group row is removed if its account group no longer has any account
  registered on the General Audit; a row for a group still in use is kept as is (not
  duplicated), with its computed amounts refreshed. Total rows are never removed.
- The **Audit Opinion** tab and its fields are unaffected. That tab shows three sections
  — Opinion on Financial Statement, Opinion on Compliance with Laws and Regulations, and
  Opinion on Compliance with Internal Control — each with an opinion and a date; the
  Opinion on Financial Statement is read-only and shows the opinion and date of the
  General Audit, and the two Compliance sections are local to this worksheet. None of
  them is changed by Reload.
