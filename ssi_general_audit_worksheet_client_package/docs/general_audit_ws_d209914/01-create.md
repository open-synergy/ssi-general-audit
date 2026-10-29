# Create General Ledger

> **Module:** `ssi_general_audit_worksheet_client_package`\
> **Model:** `general_audit_ws_d209914`\
> **Menu:** Risk Assessment > Client Assistance Package > General Ledgers\
> **Actor:** user in group _General Ledger (d209914) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** Fewer than 100 `general_audit_ws_d209914` worksheets exist for that General
  Audit (up to 100 of this kind are allowed per General Audit).
- **Access:** User is in group _General Ledger (d209914) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Client Assistance Package > General Ledgers** menu. If
   **Client Assistance Package** is not visible in the top menu bar, click the **+**
   button at its right end first. The menu list that opens shows **Client Assistance
   Package** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
