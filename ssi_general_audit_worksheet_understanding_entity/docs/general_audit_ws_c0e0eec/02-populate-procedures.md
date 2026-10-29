# Populate Procedures — Fraud Factor Analysis

> **Module:** `ssi_general_audit_worksheet_understanding_entity`\
> **Model:** `general_audit_ws_c0e0eec`\
> **Menu:** Risk Assessment > Understanding The Entity > Fraud Factor Analysis\
> **Actor:** user in group _Fraud Factor Analysis (c0e0eec) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Config:** Fraud factor indicators exist in the master data (they are installed with
  the module).
- **Access:** User is in group _Fraud Factor Analysis (c0e0eec) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Understanding The Entity > Fraud Factor Analysis** menu.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Procedures** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **Details** tab has one row for every fraud factor indicator in the master data;
  rows already present are kept, and rows whose indicator no longer exists are removed.
- Clicking **Procedures** again does not duplicate rows.
