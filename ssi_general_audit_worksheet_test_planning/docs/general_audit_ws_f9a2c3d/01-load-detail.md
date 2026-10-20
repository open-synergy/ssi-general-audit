# Load Detail — Test of Detail Planning (f9a2c3d)

> **Module:** `ssi_general_audit_worksheet_test_planning`\
> **Model:** `general_audit_ws_f9a2c3d`\
> **Menu:** Risk Responses > Substantive Test > Test of Detail Planning\
> **Actor:** user in group _Test of Detail Planning (f9a2c3d) — User_

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Data:** The related General Audit has one or more standard accounts
  (`general_audit.standard_detail`).
- **Data:** To get a balance and a performance materiality, the Specific Materiality
  worksheet (6dcda0e) of the same General Audit has a line for the account. Without that
  line the balance is 0.0 and the performance materiality is the **Balance** of the
  Specific Materiality worksheet.
- **Data:** To get an AP Result, the Analytical Procedures – Cycle worksheet (a3c9d2e)
  has a result for the account. Without a result the AP Result is **None**.
- **Access:** User is in group _Test of Detail Planning (f9a2c3d) — User_ (or higher).

## Flow

1. Open the **Risk Responses > Substantive Test > Test of Detail Planning** menu.
2. Open the worksheet to load the lines for.
3. Open the **Details** tab (the first tab).
4. Click the **Detail** button.

## Post-Condition

- The **Details** table is rebuilt with one line per standard account of the General
  Audit. Pressing **Detail** again does not duplicate the lines: it removes them and
  creates them again, so the **Timing**, **Extent** and **Primary Audit Technique**
  chosen before are cleared.
- Each line shows these columns, none of them editable by hand:
  - **Standard Account** and **Account Type**.
  - **Balance**: the balance of the account in the Specific Materiality worksheet
    (6dcda0e).
  - **Performance Materiality**: the specific materiality of the account when **Use
    Specific Materiality** is ticked in the Specific Materiality worksheet; otherwise
    the **Balance** of that worksheet, which follows its Materiality Type.
  - **ROMM** and **Assersion Types** of the account, from the Account Level ROMM
    worksheet.
  - **AP Result**: High or Moderate from the Analytical Procedures – Cycle worksheet, or
    **None** when the account has no result.
- **Timing**, **Extent** and **Primary Audit Technique** are empty (see
  `02-isi-perencanaan`).
