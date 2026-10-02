# Create Adjusting CoA

> **Module:** `ssi_general_audit`\
> **Model:** `client_adjusting_coa`\
> **Menu:** Risk Responses > Result > Adjusting CoA\
> **Actor:** Adjusting CoA user\
> **State:** `—` → `draft`

## Pre-Condition

- **Record:** A General Audit exists and is in **On Progress** status.
- **Data:** An account type set is assigned to the General Audit, and it contains the
  account type of each new account.
- **Access:** User belongs to the _User_ group of the **Adjusting CoA** workflow
  category.
- **Access:** User belongs to a data ownership group of the **Adjusting CoA** category
  (_Operating Unit_, _Company_, _Company and All Child Companies_, or _All_). Without it
  the record rules refuse the new document unless the user is the Responsible, the
  Reviewer, or the responsible or reviewer of the General Audit.

## Flow

1. Open the **Risk Responses > Result > Adjusting CoA** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **# General Audit**: Select the running General Audit that receives the new
     accounts.
4. On the **Details** tab, add one line for each new account:
   - **Code**: Code of the new account. It must not exist yet for the client.
   - **Name**: Name of the new account.
   - **Type**: Account type of the new account. Only types in the account type set of
     the General Audit are offered.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- No client account is created yet. The accounts are created when the document is done.
