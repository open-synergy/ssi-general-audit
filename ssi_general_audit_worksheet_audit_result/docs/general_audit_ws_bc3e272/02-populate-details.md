# Populate Details — Audit Result Discussion

> **Module:** `ssi_general_audit_worksheet_audit_result`\
> **Model:** `general_audit_ws_bc3e272`\
> **Menu:** Windup & Reporting > Audit Result > Audit Result Discussion\
> **Actor:** user in group _Audit Result Discussion (bc3e272) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The General Audit has _Findings That Influence Opinion_ and/or _Control
  Deficiencies_ detail lines.
- **Access:** User is in group _Audit Result Discussion (bc3e272) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Audit Result > Audit Result Discussion** menu.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Findings That Influence Opinion** and **Control Deficiencies** sections have one
  line for every upstream detail line of the same General Audit; existing lines are kept
  and lines whose source no longer exists are removed.
- Clicking **Populate** again does not duplicate lines.
