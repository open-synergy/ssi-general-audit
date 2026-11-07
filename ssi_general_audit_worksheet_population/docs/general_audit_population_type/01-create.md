# Create Population Type

> **Module:** `ssi_general_audit_worksheet_population`\
> **Model:** `general_audit_population_type`\
> **Menu:** Configuration > Standard & Regulation > Population Types\
> **Actor:** user in group _Population Type_\
> **State:** `—` → `—`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Population Type_.

## Flow

1. Open the **Configuration > Standard & Regulation > Population Types** menu. If
   **Standard & Regulation** is not visible in the top menu bar, click the **+** button
   at its right end first. The menu list that opens shows **Standard & Regulation** with
   its entries below it.
2. Click the **Create** button. _(16.0 and later: "New")_
3. Fill in the required fields:
   - **Name**: name of the population type.
   - **Code**: unique identifier. Type `/` if no identifier is needed.
4. Optionally click **Generate Code** to let the system assign the **Code** from a
   sequence template, when one is set for this master data. Only a record whose code is
   `/` gets a generated code.
5. Click **Save**.

## Post-Condition

- A new Population Type is created and is **Active**.
- The type can be selected on a new Population worksheet.
