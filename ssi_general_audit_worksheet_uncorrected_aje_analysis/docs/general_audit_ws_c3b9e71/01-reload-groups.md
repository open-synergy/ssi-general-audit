# Reload Groups and Review Uncorrected AJE — Uncorrected AJE Analysis

> **Module:** `ssi_general_audit_worksheet_uncorrected_aje_analysis`
>
> **Model:** `general_audit_ws_c3b9e71`
>
> **Menu:** Risk Responses > Result > Uncorrected AJE Analysis
>
> **Actor:** user in group _Uncorrected AJE Analysis (c3b9e71) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** the audit has at least one Adjusting Journal Entry in **Done** status whose
  **Corrected** box is unchecked; only those entries are analysed.
- **Data:** the audit has a Specific Materiality worksheet with a Performance
  Materiality; without it, **Performance Materiality** is zero and every uncorrected
  amount is shown as material.
- **Config:** each account group of the audit has a **Report Category**, and the audit
  has its account group details loaded.
- **Access:** User is in group _Uncorrected AJE Analysis (c3b9e71) — User_ (or higher).

## Flow

1. Open the **Risk Responses > Result > Uncorrected AJE Analysis** menu.
2. Open the worksheet to analyse.
3. In the **Analysis** tab, enter the **Tax Rate (%)**.
4. Click the **Reload Groups** button.
5. Open the **Links** tab.
6. Click the **Open Uncorrected AJE** button to review the entries behind the figures.
   The list and form that open are read-only.

## Post-Condition

- The **Account Groups** table of the **Analysis** tab is rebuilt with one row per
  account group of the audit: the audited **Balance**, the **Uncorrected Amount**, and
  its percentage of the balance and of Performance Materiality.
- **Pre-Tax Impact on Profit** and **Post-Tax Impact on Profit** are recomputed, the
  latter using the entered tax rate, and **Materiality Conclusion** shows whether the
  absolute after-tax impact is greater than Performance Materiality.
- The **Links** tab lists the Done, uncorrected Adjusting Journal Entries of the audit.
  It updates by itself; only the **Account Groups** table needs **Reload Groups** after
  an entry changes.
