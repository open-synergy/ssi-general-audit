# Reload Ratio — Ratio Analysis

> **Module:** `ssi_general_audit_worksheet_final_materiality`\
> **Model:** `general_audit_ws_f3a78de`\
> **Menu:** Windup & Reporting > Final Analysis > Final Analytical Procedures > Ratio
> Analysis\
> **Actor:** user in group _Final Analytical Procedures - Ratio Analysis — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** Financial ratios are defined in the client financial ratio master.
- **Access:** User is in group _Final Analytical Procedures - Ratio Analysis — User_ (or
  higher).

## Flow

1. Open the **Windup & Reporting > Final Analysis > Final Analytical Procedures > Ratio
   Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Ratios** tab.
4. Click the **Detail** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Ratios** tab has one line for every financial ratio in the master; existing
  lines are kept and lines whose ratio is no longer in the master are removed.
- New lines take the industry average and analysis of the matching ratio line of the
  linked Preliminary Analytic Procedure - Ratio Analysis worksheet, if any.
- The amounts of all ratio lines are recomputed, so a separate **Compute** is not needed
  right after **Detail** (see `03-compute-ratio`).
- Clicking **Detail** again does not duplicate lines.
