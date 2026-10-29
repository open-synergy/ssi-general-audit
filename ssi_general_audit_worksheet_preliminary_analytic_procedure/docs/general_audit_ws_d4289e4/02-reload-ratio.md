# Reload Ratio — Ratio Analysis

> **Module:** `ssi_general_audit_worksheet_preliminary_analytic_procedure`\
> **Model:** `general_audit_ws_d4289e4`\
> **Menu:** Risk Assessment > Analytical Procedures > Preliminary Analytic Procedures -
> Ratio Analysis\
> **Actor:** user in group _Preliminary Analytic Procedure - Ratio Analysis — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** Financial ratios are defined in the client financial ratio master.
- **Access:** User is in group _Preliminary Analytic Procedure - Ratio Analysis — User_
  (or higher).

## Flow

1. Open the **Risk Assessment > Analytical Procedures > Preliminary Analytic
   Procedures - Ratio Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Ratios** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Ratios** tab has one line for every financial ratio in the master; existing
  lines are kept and lines whose ratio is no longer in the master are removed.
- The amounts of all ratio lines are recomputed, so a separate **Compute** is not needed
  right after **Reload** (see `03-compute-ratio`).
- Clicking **Reload** again does not duplicate lines.
