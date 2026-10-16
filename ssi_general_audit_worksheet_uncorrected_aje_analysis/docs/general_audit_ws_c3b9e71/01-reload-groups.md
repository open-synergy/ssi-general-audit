# Reload Groups and Review Uncorrected AJE — Uncorrected AJE Analysis

> **Module:** `ssi_general_audit_worksheet_uncorrected_aje_analysis`
>
> **Model:** `general_audit_ws_c3b9e71`
>
> **Menu:** Windup & Reporting > Final Analysis > Uncorrected AJE Analysis
>
> **Actor:** user in group _Uncorrected AJE Analysis (c3b9e71) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** the audit has at least one Adjusting Journal Entry in **Done** status whose
  **Corrected** box is unchecked; only those entries are analysed.
- **Data:** the audit has a Final Materiality worksheet that is not cancelled; without
  it, **Overall Materiality**, **Performance Materiality** and **Clearly Trivial** are
  zero and every uncorrected amount is shown as material.
- **Data:** the audit has a Specific Materiality worksheet whose mapping lines carry the
  audited balance of each account group.
- **Config:** each account group of the audit has a **Report Category**, and the audit
  has its account group details loaded.
- **Access:** User is in group _Uncorrected AJE Analysis (c3b9e71) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Final Analysis > Uncorrected AJE Analysis** menu.
2. Open the worksheet to analyse.
3. In the **Quantification** tab, click the **Reload Groups** button.
4. Open the **Analysis** tab.
5. In **Analysis - Aggregate**, enter the **Tax Rate (%)**.
6. Open the **Links** tab.
7. Click the **Open Uncorrected AJE** button to review the entries behind the figures.
   The list and form that open are read-only.

## Post-Condition

- The **Quantification** tab shows **Overall Materiality**, **Performance Materiality**
  and **Clearly Trivial** of the Final Materiality worksheet, with a link to it.
- The **Account Groups** table of the **Quantification** tab is rebuilt with one row per
  account group of the audit: the audited **Balance**, the **Uncorrected Misstatement**,
  the **Balance After Misstatement**, and its percentage of the balance and of
  Performance Materiality.
- **Analysis - Aggregate** is recomputed: the net uncorrected misstatement on profit or
  loss, the **Net Impact After Tax** using the entered tax rate, and the total of one
  side (debit or credit) of the uncorrected Adjusting Journal Entries for the statement
  of financial position, each with its percentage of Performance Materiality.
- The **Links** tab lists the Done, uncorrected Adjusting Journal Entries of the audit.
  It updates by itself; only the **Account Groups** table needs **Reload Groups** after
  an entry changes.
