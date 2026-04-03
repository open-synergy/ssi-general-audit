# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc435bcdItem(models.Model):
    """Master template for checklist items used in the Assignment Letter worksheet.

    Each record defines one verification criterion that an auditor must assess
    when reviewing the formal completeness of an Audit Assignment Letter
    (Surat Penugasan).  These records are configured once by an administrator
    and are then referenced by every ``general_audit_ws_c435bcd.checklist``
    response row that auditors fill in.

    Inherits ``mixin.checklist.item`` which provides:
    - ``name`` — description of what must be verified.
    - ``option_set_id`` — the set of allowed answer options (e.g. Yes / No / N/A).
    - ``sequence`` — display order within the checklist.

    Pre-configured items (loaded via XML data)
    ------------------------------------------
    1. Client name is presented correctly in the letter.
    2. The letter is dated in accordance with the agreement date.
    3. The letter is numbered per applicable administrative procedures.
    4. Engagement team member names match the selected audit personnel.
    5. The engagement period matches the planned schedule.
    """

    _name = "general_audit_ws_c435bcd.item"
    _inherit = [
        "mixin.checklist.item",
    ]
    _description = "Assignment Letter (c435bcd) - " "Checklist Item"

    code = fields.Char(
        default="/",
    )
