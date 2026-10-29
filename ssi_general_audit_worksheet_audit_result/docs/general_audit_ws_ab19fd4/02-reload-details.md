# Reload Details — Audit Result Formulation

> **Module:** `ssi_general_audit_worksheet_audit_result`\
> **Model:** `general_audit_ws_ab19fd4`\
> **Menu:** Windup & Reporting > Audit Result > Audit Result Formulation > Audit Result
> Formulation\
> **Actor:** user in group _Audit Result Formulation (ab19fd4) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The General Audit has a _Findings That Influence Opinion_ and/or a _Control
  Deficiencies_ worksheet. Upstream worksheets should be confirmed first.
- **Access:** User is in group _Audit Result Formulation (ab19fd4) — User_ (or higher).

## Flow

1. Open the **Windup & Reporting > Audit Result > Audit Result Formulation > Audit
   Result Formulation** menu.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Findings That Influence Opinion** and **Control Deficiencies** sections show the
  source worksheet and all detail lines of the same General Audit.
- Run **Reload** again after upstream worksheets change; the sections are refreshed, not
  duplicated.
