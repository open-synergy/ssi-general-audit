# Fill Data, Data Comparison, and Check Line

> **Module:** ssi_general_audit_worksheet_physical_check
>
> **Model:** `general_audit_ws_c7d5f2b`
>
> **Menu:** Risk Responses > General Procedures > Inspection > Physical Check
>
> **Actor:** user in group _Physical Check (c7d5f2b) — User_

## Pre-Condition

- **Record:** Status is **Open**.
- **Data:** For **Data Mode = General Ledger**: a General Ledger worksheet already
  exists for the same engagement with Raw Data imported.
- **Data:** For **Data Mode = Subledger**: a Subledger worksheet already exists for the
  same engagement with Raw Data imported.
- **Data:** For **Data Source = Sample**: a Sample Determination worksheet with a
  generated sample already exists for the same engagement, linked to the same General
  Ledger/Subledger selected by this worksheet's **Data Mode**.
- **Data:** A comparison General Ledger or Subledger worksheet (a second one, distinct
  from the population source) already exists for the same engagement with Raw Data
  imported, to be used as the Data Comparison source in this Flow.
- **Access:** User is in group _Physical Check (c7d5f2b) — User_ (or higher).

## Flow

1. Open the **Risk Responses > General Procedures > Inspection > Physical Check** menu.
2. Open the worksheet to fill in.
3. In the header, select the **Data Mode**: **General Ledger** or **Subledger**.
4. Select the matching source record: the **General Ledger** field (shown when Data Mode
   is General Ledger) or the **Subledger** field (shown when Data Mode is Subledger).
5. Select the **Data Source**:
   - **Population**: uses 100% of the General Ledger/Subledger selected in step 4
     directly.
   - **Sample**: uses the sampling result of a linked Sample Determination worksheet.
6. If **Data Source** is **Sample**: select the **# Sample Determination** field, then
   fill the **Reference Column Number** field with the sampling data column number
   holding the reference identifier.
7. Open the **Data Comparisons** tab and click the **Open Data Comparisons** button.
8. In the Data Comparisons list, click **Create** to add a comparison line. **(14.0:
   "Create")**
9. On the new Data Comparison line, select its own **Data Mode** and matching General
   Ledger/Subledger record, then fill the **Reference Column Number** field with the
   comparison raw data column holding the reference identifier. Save the line.
10. Go back to the worksheet and open the **Check** tab, then click the **Open Check
    Lines** button.
11. In the Check Lines list, click **Create** to add a check line. **(14.0: "Create")**
12. On the new Check line, select the **Data Comparison** created in step 9, select the
    **Comparison Mode** (Count/Sum/AVG), then fill the **Reference Amount Column** and
    **Comparison Amount Column** fields with the respective amount column numbers.
13. Click the **Compute Check Data** button.

## Post-Condition

- The **Check Data** field on the check line (**Check Data** tab) is filled with the CSV
  comparison result: one row per reference value with columns Ref, Amount Reference,
  Amount Comparison, Diff, and Result (`True` when Diff is zero, `False` otherwise).
- On the worksheet header, the **Check Data** page shows the population/sample subset
  used as the reference side of the comparison.
