# Populate Checklist — Financial Statement Disclosure Review (be62e79)

> **Module:** `ssi_general_audit_worksheet_review`
>
> **Model:** `general_audit_ws_be62e79`
>
> **Menu:** Windup & Reporting > Review > Financial Statement Disclosure > Financial
> Statement Disclosure
>
> **Actor:** user in group _Financial Statement Disclosure Review (be62e79) — User_
>
> **State:** open

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** At least one active checklist item exists in the disclosure review item
  master of this module. Only active items are listed by **Populate**.
- **Access:** User is in group _Financial Statement Disclosure Review (be62e79) — User_
  (or higher).

## Flow

1. Open the **Windup & Reporting > Review > Financial Statement Disclosure > Financial
   Statement Disclosure** menu.
2. Open the worksheet to prepare.
3. Open the **Checklist** tab.
4. Click **Populate**.

## Post-Condition

- The **Checklist** tab holds one row for every active checklist item, in the item
  sequence order.
- Items that already had a row keep it. **Populate** does not create duplicates.
- Rows whose item was deleted or deactivated in the master are removed.
