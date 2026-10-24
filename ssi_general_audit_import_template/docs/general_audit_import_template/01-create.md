# Create Import Template

> **Module:** `ssi_general_audit_import_template`\
> **Model:** `general_audit_import_template`\
> **Menu:** Configuration > Import Templates\
> **Actor:** Import Template configurator\
> **State:** `—` → `—`

## Pre-Condition

- **Access:** User belongs to the _General Audit Import Template Configurator_ group.
- **Data:** The target model of the template exists in the system (for example
  _Accountant Client Trial Balance_).

## Flow

1. Open the **Configuration > Import Templates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the **Name** field.
4. On the **Settings** tab, fill in the required fields:
   - **Target Model**: Select the model whose Action menu will offer the download.
   - **File Name**: Name of the downloaded file. It is filled with
     `import_template.csv`.
   - **Delimiter**: Comma or Semicolon. It is filled with Comma.
   - **Has Header**: Tick it to write the column titles as the first row.
5. On the **Columns** tab, add one line for each column of the file:
   - **Column Title**: Title of the column.
   - **Example Value**: Sample value written in the example row.
   - **Note**: Remark about the expected content.
6. Click **Save**.

## Post-Condition

- A new template is created with its columns listed on the **Columns** tab.
- No server action exists yet. The **Server Action** field is empty.
