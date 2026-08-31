# Fill Data and Generate Examination Data — Test of Detail

> **Module:** ssi_general_audit_worksheet_test_of_detail
>
> **Model:** `general_audit_ws_b4f8e1a`
>
> **Menu:** Risk Responses > Result > Test of Detail
>
> **Actor:** user in group _Test of Detail (b4f8e1a) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** For **Data Source = Population**: a General Ledger or Subledger worksheet
  already exists for the same engagement with Raw Data imported, its Identifier Column
  Number configured (used to fill the **Data** column of Examination Data; left blank
  there, that column stays empty), and, for General Ledger, its Debit/Credit column
  numbers configured.
- **Data:** For **Data Source = Sample**: a Sample Determination worksheet with a
  generated sample already exists for the same engagement, linked to the same General
  Ledger/Subledger selected by this worksheet's **Data Mode**.
- **Data:** For **Data Mode = Subledger** together with **Data Source = Population**:
  the selected Subledger worksheet has at least one Amount column configured, and its
  **Recorded Amount Column** field (Raw Data tab) is set to the amount column
  representing the recorded transaction amount.
- **Access:** User is in group _Test of Detail (b4f8e1a) — User_ (or higher).

## Flow

1. Open the **Risk Responses > Result > Test of Detail** menu.
2. Open the worksheet to fill in.
3. In the **Data** section, select the **Data Mode**: **General Ledger** or
   **Subledger**.
4. Select the matching source record: the **General Ledger** field (shown when Data Mode
   is General Ledger) or the **Subledger** field (shown when Data Mode is Subledger).
5. Select the **Data Source**:
   - **Population**: examines 100% of the General Ledger/Subledger selected in step 4
     directly.
   - **Sample**: uses the sampling result of a linked Sample Determination worksheet.
6. If **Data Source** is **Sample**: select the **# Sample Determination** field. Only
   Sample Determination worksheets linked to the same General Ledger/Subledger selected
   in step 4 are selectable.
7. Click the **Generate Examination Data** button.

## Post-Condition

- The **Examination Data** table (**Examination Data** tab) is (re)built:
  - **Sample**: one row per item sampled by the linked Sample Determination worksheet,
    carrying over its Item, Data, and Recorded Amount; Audited Amount is left blank.
  - **Population**: one row per data row (excluding header) of the selected General
    Ledger/Subledger; Data is the value of the selected General Ledger/Subledger's own
    **Identifier Column Number** column (blank if not configured there); Recorded Amount
    is Debit minus Credit (General Ledger) or the raw value of the selected Subledger's
    own **Recorded Amount Column** (Subledger); Audited Amount is left blank.
- Any Audited Amount values entered before this action are discarded and must be
  re-entered.
