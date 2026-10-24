# Create Server Action

> **Module:** `ssi_general_audit_import_template`\
> **Model:** `general_audit_import_template`\
> **Menu:** Configuration > Import Templates\
> **Actor:** Import Template configurator\
> **Requires:** `01-create`\
> **Inline Actions:** Remove Server Action

## Pre-Condition

- **Record:** An import template exists, is saved, and has no server action.
- **Access:** User belongs to the _General Audit Import Template Configurator_ group.

## Flow

1. Open the **Configuration > Import Templates** menu.
2. Open the template.
3. Click the **Create Server Action** button.
4. To undo it later, click the **Remove Server Action** button and confirm.

## Post-Condition

- The **Server Action** field on the **Settings** tab is filled.
- The **Create Server Action** button is replaced by **Remove Server Action**.
- The Action menu of the target model offers "Download Template: <name>". Clicking it
  downloads the CSV file.
- The **Target Model** can not be changed until the server action is removed.
- Clicking **Remove Server Action**, or deleting the template, removes the entry from
  the Action menu.
