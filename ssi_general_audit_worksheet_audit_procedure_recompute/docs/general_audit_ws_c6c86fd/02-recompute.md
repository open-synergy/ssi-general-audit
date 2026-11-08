# Recompute — Recompute Audit Procedure

> **Module:** `ssi_general_audit_worksheet_audit_procedure_recompute`\
> **Model:** `general_audit_ws_c6c86fd`\
> **Menu:** Risk Responses > General Procedures > Recompute\
> **Actor:** user in group _Recompute Audit Procedure (c6c86fd) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The worksheet has a **General Ledger** or **Subledger** (and, for **Sample**
  data source, a **Sample Determination**) selected, so that **Raw Data** is not empty.
- **Data:** On the **Recompute Configuration** tab, **Ref Column Number** and **Original
  Amount Column Number** are filled.
- **Data:** On the **Recompute Formula** tab, **Recompute Formula** is filled (for
  example `col_3 + col_4 - col_5`).
- **Access:** User is in group _Recompute Audit Procedure (c6c86fd) — User_ or higher.

## Flow

1. Open the **Risk Responses > General Procedures > Recompute** menu. If **General
   Procedures** is not visible in the top menu bar, click the **+** button at its right
   end first.
2. Open the worksheet to work on.
3. Open the **Recompute Formula** tab.
4. Click the **Recompute** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- **Recompute Data** is filled with a comparison table that has the columns Ref,
  Original Amount, Recompute Amount, Diff and Result (**Ok** or **Not Ok**).
- A row is **Ok** when the difference is within **Tolerable Amount**.
- The status stays **On Progress**.
