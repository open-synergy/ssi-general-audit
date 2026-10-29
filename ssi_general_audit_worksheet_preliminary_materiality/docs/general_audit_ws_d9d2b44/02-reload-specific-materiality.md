# Reload Specific Materiality Link — Materiality Computation

> **Module:** `ssi_general_audit_worksheet_preliminary_materiality`\
> **Model:** `general_audit_ws_d9d2b44`\
> **Menu:** Risk Assessment > Materiality > Materiality Computation\
> **Actor:** user in group _Materiality Computation — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** A Specific Materiality worksheet that uses this Materiality Computation as
  its base exists (see `general_audit_ws_6dcda0e/01-create`).
- **Access:** User is in group _Materiality Computation — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Materiality > Materiality Computation** menu.
2. Open the worksheet to work on.
3. Open the **Materiality** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The **# Specific Materiality Worksheet** field in the **Overview** group shows the
  Specific Materiality worksheet that points back to this Materiality Computation.
