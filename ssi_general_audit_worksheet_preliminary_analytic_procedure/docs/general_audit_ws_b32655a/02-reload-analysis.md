# Reload Analysis — Vertical and Horizontal Analysis

> **Module:** `ssi_general_audit_worksheet_preliminary_analytic_procedure`\
> **Model:** `general_audit_ws_b32655a`\
> **Menu:** Risk Assessment > Analytical Procedures > Analytic Procedures - Vertical and
> Horizontal Analysis\
> **Actor:** user in group _Preliminary Analytic Procedure - Vertical and Horizontal Analysis
> — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** The General Audit has standard details (the account types of its standard).
- **Access:** User is in group _Preliminary Analytic Procedure - Vertical and Horizontal
  Analysis — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Analytical Procedures > Analytic Procedures - Vertical
   and Horizontal Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Analysis** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Analysis** tab has one line for every standard detail of the General Audit;
  existing lines are kept and lines whose standard detail no longer exists are removed.
- Clicking **Reload** again does not duplicate lines.
