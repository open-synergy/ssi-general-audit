# Load Analysis — Vertical and Horisontal Analysis

> **Module:** `ssi_general_audit_worksheet_final_materiality`\
> **Model:** `general_audit_ws_e1f2d98`\
> **Menu:** Windup & Reporting > Final Analysis > Final Analytical Procedures > Vertical
> and Horisontal Analysis\
> **Actor:** user in group _Final Analytical Procedures - Vertical and Horisontal Analysis
> — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** A Preliminary Analytic Procedure - Vertical and Horizontal Analysis
  worksheet (`general_audit_ws_b32655a`) of the same General Audit exists and is
  selected in the **# Preliminary Analytic Procedure** field of the tab.
- **Access:** User is in group _Final Analytical Procedures - Vertical and Horisontal
  Analysis — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Final Analysis > Final Analytical Procedures >
   Vertical and Horisontal Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Vertical and Horisontal Analysis** tab.
4. Click the **Detail** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Vertical and Horisontal Analysis** tab has one line for every analysis line of
  the selected preliminary worksheet; existing lines are kept and lines that no longer
  exist there are removed.
- Clicking **Detail** again does not duplicate lines.
