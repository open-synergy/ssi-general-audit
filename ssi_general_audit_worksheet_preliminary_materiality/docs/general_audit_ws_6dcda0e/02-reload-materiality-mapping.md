# Reload Materiality Mapping — Specific Materiality

> **Module:** `ssi_general_audit_worksheet_preliminary_materiality`\
> **Model:** `general_audit_ws_6dcda0e`\
> **Menu:** Risk Assessment > Materiality > Specific Materiality\
> **Actor:** user in group _Specific Materiality — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden in every other
  status.
- **Data:** The General Audit has standard details (the account types of its standard).
- **Access:** User is in group _Specific Materiality — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Materiality > Specific Materiality** menu.
2. Open the worksheet to work on.
3. Open the **Materiality** tab.
4. Click the **Reload** button. The button is only visible while the status is **On
   Progress**.

## Post-Condition

- The materiality mapping lines on the **Materiality** tab have one line for every
  standard detail of the General Audit; existing lines are kept and lines whose standard
  detail no longer exists are removed.
- Clicking **Reload** again does not duplicate lines.
