# Import Client Accounts

> **Module:** `ssi_general_audit`\
> **Model:** `import_client_account`\
> **Menu:** Risk Assessment > Trial Balance > CoA and Mapping\
> **Actor:** CoA and Mapping user\
> **State:** `open` → `open`

## Pre-Condition

- **Record:** A CoA and Mapping document exists and is in **Open** status. The **Import
  Accounts** button is hidden in any other status.
- **Data:** A CSV file is ready, in UTF-8, with one row per account and the columns
  account code, account name, an unused column, and the standard account type code, in
  that order. The first row is a header row, unless **File Has Header Row** is
  unchecked.
- **Access:** User belongs to the _User_ group of the **Client Account Mapping**
  workflow category, or is the Responsible of the document.

## Flow

1. Open the **Risk Assessment > Trial Balance > CoA and Mapping** menu.
2. Open the Open record that receives the accounts.
3. On the **Account Mappings** tab, click the **Import Accounts** button.
4. In the **Import Client Account** dialog, select the CSV file in **File**.
   - The **Import Preview** shows the client name, the number of valid rows, and the
     number of rows to be skipped. Nothing is created yet.
   - Uncheck **File Has Header Row** if the file has no header row.
5. Click **Import** in the dialog footer.
6. Read the notification that reports how many rows were imported, updated, and skipped.
   - If a new account has the same name as another account of the client, the
     notification also lists the duplicate names.
7. Check the **Account Mappings** tab for the new lines.

## Post-Condition

- The dialog is closed and the record stays in **Open** status.
- A new client account is created for each row whose code is new for the client, and the
  existing account is reused for a code that already exists.
- Each valid row is listed on the **Account Mappings** tab.
- Rows with an empty code, a code longer than 32 characters, and the header row are
  skipped and not created.
