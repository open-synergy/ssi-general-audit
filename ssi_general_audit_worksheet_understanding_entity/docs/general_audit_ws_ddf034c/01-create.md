# Create General Information and Legal Aspect

> **Module:** `ssi_general_audit_worksheet_understanding_entity`\
> **Model:** `general_audit_ws_ddf034c`\
> **Menu:** Risk Assessment > Understanding The Entity > General Information and Legal
> Aspect\
> **Actor:** user in group _General Information and Legal Aspec (ddf034c) — User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `general_audit` record exists and is in status **Open**.
- **Data:** No `general_audit_ws_ddf034c` worksheet exists yet for that General Audit
  (only one worksheet of this kind is allowed per General Audit).
- **Access:** User is in group _General Information and Legal Aspec (ddf034c) — User_ or
  higher.

## Flow

1. Open the **Risk Assessment > Understanding The Entity > General Information and Legal
   Aspect** menu.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required field:
   - **General Audit**: select the open `general_audit` engagement this worksheet
     belongs to.
4. **Accountant**, **Partner**, and **Title** are automatically filled from the selected
   **General Audit**.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Client Contacts**, **Establishment of the Company**, **Amendment of Deeds**,
  **Other Legalities** and **Building Status** tabs are empty.
