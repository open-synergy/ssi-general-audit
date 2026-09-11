# Edit Financial Statement Disclosure (a025441)

> **Module:** ssi*general_audit_worksheet_review **Model:** `general_audit_ws_a025441` >
> **Menu:** Windup & Reporting > Review > Financial Statement Disclosure **Actor:** user
> in group \_Financial Statement Disclosure (a025441) — User* (or higher)

## Pre-Condition

- **Record:** Status is **Open**. `raw_data`, `conclusion_id`, and `conclusion` are
  editable only while the worksheet is Open; outside that state they are read-only. All
  three are inherited generically from the base worksheet (`general_audit_worksheet`)
  except `raw_data`, which this module adds. `financial_accounting_standard_id` is
  always read-only (related from the parent General Audit).
- **Data:** A General Audit engagement already exists and is Open, with a worksheet of
  this type already created for it. Its **Financial Accounting Standard** (e.g. IFRS,
  PSAK Umum, PSAK ETAP) is set, since the worksheet shows it for reference.
- **Data:** The auditor has completed the financial statement disclosure checklist for
  the applicable financial reporting framework (e.g. IFRS, PSAK Umum, PSAK ETAP) outside
  Odoo (e.g. in a spreadsheet) and exported it as CSV.
- **Data:** Conclusion master data for this worksheet type already exists (shipped by
  the module, e.g. "Financial Statement Disclosure has been completed" / "... has not
  been completed").
- **Access:** User is in group _Financial Statement Disclosure (a025441) — User_ (or
  higher).

## Flow

1. Open the **Windup & Reporting > Review > Financial Statement Disclosure** menu.
2. Open the worksheet to fill in. The **Financial Accounting Standard** field (below
   Reviewer) shows which checklist variant applies.
3. Click the **Edit** button.
4. Open the **Checklist** tab (the first tab), then paste the completed disclosure
   checklist CSV (item, source standard, note, and Yes/No/N-A status per row) into the
   **Raw Data** field.
5. Select the **Conclusion** field (e.g. "Financial Statement Disclosure has been
   completed"), based on whether all required disclosures were made.
6. Fill in the **Conclusion** narrative text field with a summary of the completeness
   assessment.
7. Click **Save**.

## Post-Condition

- The worksheet's **Raw Data**, **Conclusion**, and **Conclusion** narrative fields are
  updated with the new values.
- The fields remain editable as long as the worksheet stays **Open**; once the worksheet
  leaves the Open state (e.g. Confirm), they become read-only again.
