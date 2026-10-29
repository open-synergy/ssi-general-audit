# Compute Ratio — Ratio Analysis

> **Module:** `ssi_general_audit_worksheet_final_materiality`\
> **Model:** `general_audit_ws_f3a78de`\
> **Menu:** Windup & Reporting > Final Analysis > Final Analytical Procedures > Ratio
> Analysis\
> **Actor:** user in group _Final Analytical Procedures - Ratio Analysis — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** The **Ratios** tab already has lines (see `02-reload-ratio`).
- **Access:** User is in group _Final Analytical Procedures - Ratio Analysis — User_ (or
  higher).

## Flow

1. Open the **Windup & Reporting > Final Analysis > Final Analytical Procedures > Ratio
   Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Ratios** tab.
4. Click the **Compute** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The amounts of every ratio line are recalculated from the current figures of the
  General Audit.
- Run **Compute** again after the General Audit figures change.
