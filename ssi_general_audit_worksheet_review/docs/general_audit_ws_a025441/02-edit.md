# Edit Financial Statement Disclosure (a025441)

> **Module:** ssi*general_audit_worksheet_review **Model:** `general_audit_ws_a025441` >
> **Menu:** Windup & Reporting > Review > Financial Statement Disclosure **Actor:** user
> in group \_Financial Statement Disclosure (a025441) — User* (or higher)

## Pre-Condition

- **Record:** Status is **Open**. `raw_data` and `conclusion` are editable only while
  the worksheet is Open; outside that state they are read-only. Both are inherited
  generically from the base worksheet (`general_audit_worksheet`) except `raw_data`,
  which this module adds.
- **Data:** A General Audit engagement already exists and is Open, with a worksheet of
  this type already created for it.
- **Data:** The auditor has completed the financial statement disclosure checklist for
  the applicable financial reporting framework (e.g. IFRS, PSAK Umum, PSAK ETAP) outside
  Odoo (e.g. in a spreadsheet) and exported it as CSV.
- **Access:** User is in group _Financial Statement Disclosure (a025441) — User_ (or
  higher).

## Flow

1. Open the **Windup & Reporting > Review > Financial Statement Disclosure** menu.
2. Open the worksheet to fill in.
3. Click the **Edit** button.
4. Paste the completed disclosure checklist CSV (item, source standard, note, and
   Yes/No/N-A status per row) into the **Raw Data** field.
5. Fill in the **Conclusion** narrative text field with a summary of the completeness
   assessment.
6. Click **Save**.

## Post-Condition

- The worksheet's **Raw Data** and **Conclusion** narrative fields are updated with the
  new values.
- The fields remain editable as long as the worksheet stays **Open**; once the worksheet
  leaves the Open state (e.g. Confirm), they become read-only again.

> This Post-Condition is verified at the ORM level (YAML unit test), not through the UI
> tour: re-rendering `raw_data` (widget `csv_table`, module `ssi_web_widget_csv_table`)
> after Save could not be exercised reliably in the tour environment, for reasons
> documented in the tour file itself. The tour covers Flow steps 1-6 up to clicking
> Save.

> The worksheet also carries a **Conclusion** selection field (`conclusion_id`,
> inherited generically from the base worksheet, with master data shipped by this module
> e.g. "Financial Statement Disclosure has been completed" / "... has not been
> completed") — out of scope for this Flow; see the base worksheet's own documentation.
