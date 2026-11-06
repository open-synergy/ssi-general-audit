# Populate Details — Control Risk - Entity Level

> **Module:** `ssi_general_audit_worksheet_control_risk`\
> **Model:** `general_audit_ws_b59b886`\
> **Menu:** Risk Assessment > Control Risk > Control Risk - Entity Level > Control
> Risk - Entity Level\
> **Actor:** user in group _Control Risk - Entity Level (b59b886) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** General Control Evaluation or IT Control Evaluation worksheets exist for the
  same General Audit.
- **Access:** User is in group _Control Risk - Entity Level (b59b886) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Control Risk > Control Risk - Entity Level > Control
   Risk - Entity Level** menu. If **Control Risk** is not visible in the top menu bar,
   click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Populate** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab lists one line for every General Control Evaluation and IT Control Evaluation
  worksheet of the same General Audit; lines that already exist are kept.
- Lines whose evaluation worksheet no longer exists for the General Audit are removed.
- Clicking **Populate** again does not duplicate lines.
