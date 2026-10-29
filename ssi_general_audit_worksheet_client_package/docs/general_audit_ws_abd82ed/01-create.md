# Create Client Assistance Package

> **Module:** `ssi_general_audit_worksheet_client_package`\
> **Model:** `general_audit_ws_abd82ed`\
> **Menu:** Risk Assessment > Client Assistance Package > Client Assistance Package\
> **Actor:** user in group _Client Assistance Package (abd82ed) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_abd82ed` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _Client Assistance Package (abd82ed) — User_ or higher.

## Flow

1. Open the **Risk Assessment > Client Assistance Package > Client Assistance Package**
   menu. If **Client Assistance Package** is not visible in the top menu bar, click the
   **+** button at its right end first. The menu list that opens shows **Client
   Assistance Package** with its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
