# Load Details — General Control Evaluation

> **Module:** `ssi_general_audit_worksheet_control_risk`\
> **Model:** `general_audit_ws_d3d2719`\
> **Menu:** Risk Assessment > Control Risk > Control Risk - Entity Level > General
> Control Evaluations\
> **Actor:** user in group _General Control Evaluation (d3d2719) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`).
- **Data:** The **General Control Set** field is filled, and the set has at least one
  general control.
- **Access:** User is in group _General Control Evaluation (d3d2719) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Control Risk > Control Risk - Entity Level > General
   Control Evaluations** menu. If **Control Risk** is not visible in the top menu bar,
   click the **+** button at its right end first.
2. Open the worksheet to work on.
3. Open the **Control** tab.
4. Click the **Detail** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The tab has one line for every general control in the selected set, each with a line
  for every indicator of that control.
- The tab is synchronised with the selected set. A line is added for every general
  control or indicator that has none, and the line of a general control or indicator
  that is no longer in the set is removed. All other lines are kept, so the **Result**
  and **Explanation** already entered on them are not lost.
- Clicking **Detail** again without changes alters nothing and does not duplicate lines.
