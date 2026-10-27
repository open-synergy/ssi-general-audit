# Import Adjusting Journal Lines

> **Module:** `ssi_general_audit`\
> **Model:** `client_adjustment_entry`\
> **Menu:** Risk Responses > Result > Adjusting Journal\
> **Actor:** Responsible user, reviewer, or audit responsible user\
> **State:** `draft` → `draft`

## Pre-Condition

- **Record:** An Adjusting Journal exists and is in **Draft** status.
- **Data:** The chart of accounts of the client of the General Audit contains every
  account code that the CSV file refers to.
- **Data:** A CSV file is ready, in UTF-8, with one row per line and the columns account
  code, AJE code, description, debit, and credit, in that order. The first row is a
  header row, unless **File Has Header Row** is unchecked.
- **Access:** User is the Responsible or the Reviewer of the Adjusting Journal, or the
  Responsible or Reviewer of its General Audit.

## Flow

1. Open the **Risk Responses > Result > Adjusting Journal** menu.
2. Open the Draft record that receives the lines.
3. On the **Details** tab, click the **Import** button.
4. In the **Import Adjustment Entry Detail** dialog, select the CSV file in **File**.
   - The **Import Preview** shows the client name, the number of lines to be created,
     and the number of rows with an unknown account code.
   - Uncheck **File Has Header Row** if the file has no header row.
5. Click **Import** in the dialog footer.
6. Check the **Details** tab for the new lines.

## Post-Condition

- The dialog is closed and the record stays in **Draft** status.
- One new line is listed on the **Details** tab for each imported row.
- Existing lines are not changed.
- If an account code is not found for the client, an error is shown and no line is
  created.
