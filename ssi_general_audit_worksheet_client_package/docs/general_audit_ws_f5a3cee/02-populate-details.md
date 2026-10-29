# Populate Details — Data Collection

> **Module:** `ssi_general_audit_worksheet_client_package`\
> **Model:** `general_audit_ws_f5a3cee`\
> **Menu:** Risk Assessment > Client Assistance Package > Data Collection\
> **Actor:** user in group _Data Collection (f5a3cee) — User_

## Pre-Condition

- **Record:** Status is **On Progress** (`open`). The button is hidden only in
  **Draft**.
- **Data:** The client of the General Audit has an account mapping with account types.
- **Access:** User is in group _Data Collection (f5a3cee) — User_ (or higher).

## Flow

1. Open the **Risk Assessment > Client Assistance Package > Data Collection** menu.
2. Open the worksheet to work on.
3. Open the **Details** tab.
4. Click the **Populate** button. The button is not visible while the status is
   **Draft**.

## Post-Condition

- The **Details** tab has one line for every account type in the client's account
  mapping; existing lines are kept and lines whose account type is no longer mapped are
  removed.
- Clicking **Populate** again does not duplicate lines.
