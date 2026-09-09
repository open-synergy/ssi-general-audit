# Reload Posture — Audit Result (ff42fdc)

> **Module:** ssi_general_audit_worksheet_draft_reporting
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
  - Nine fixed **Total** rows (Total Asset, Total Liability, Total Equity, Total
    Liability and Equity, Gross Profit, Operating Profit, Profit Before Tax, Profit
    After Tax, Comprehensive Profit), interleaved right after their component Account
    Group rows and shown in **bold**. Total rows always appear, even when their
    component account groups have no data.
- An Account Group row is removed if its account group no longer has any account
  registered on the General Audit; a row for a group still in use is kept as is (not
  duplicated), with its computed amounts refreshed. Total rows are never removed.
- The **Audit Opinion** tab and its fields are unaffected. That tab shows three sections
  — Opinion on Financial Statement, Opinion on Compliance with Laws and Regulations, and
  Opinion on Compliance with Internal Control — each with an opinion and a date; the two
  Compliance sections are local to this worksheet and are not changed by Reload.
