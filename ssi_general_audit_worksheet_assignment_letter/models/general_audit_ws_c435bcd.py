# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSc435bcd(models.Model):
    """Worksheet to verify the completeness and quality of the Audit Assignment
    Letter (Surat Penugasan) issued to the client before fieldwork begins.

    This worksheet is part of the pre-engagement (PE) phase and ensures the
    Assignment Letter meets the formal requirements mandated by **SA 300**
    (Planning an Audit of Financial Statements) and **SA 220** (Quality
    Control for an Audit of Financial Statements).

    The auditor reviews five formal criteria of the assignment letter via a
    structured checklist (``checklist_ids``) and records a conclusion:

    - **Assignment Letter is sufficient** — all formal requirements are met
      and the engagement can proceed.
    - **Assignment Letter is not sufficient** — one or more formal requirements
      are unmet; corrective action must be taken before the engagement
      is confirmed.

    Architecture
    ------------
    Follows the two-layer worksheet pattern used across this repository:

    - Inherits ``general_audit_worksheet_mixin`` which, via ``_inherits``,
      delegates common fields (``general_audit_id``, ``partner_id``,
      ``conclusion_id``, ``preparation_date``, etc.) to the shadow record
      ``general_audit_worksheet``.
    - Inherits ``mixin.checklist`` to support structured checklist evaluation
      through ``general_audit_ws_c435bcd.checklist`` entries backed by
      ``general_audit_ws_c435bcd.item`` templates.

    Checklist Items
    ---------------
    1. Client name is presented correctly in the letter.
    2. The letter is dated in accordance with the agreement date.
    3. The letter is numbered per applicable administrative procedures.
    4. Engagement team member names match the selected audit personnel.
    5. The engagement period matches the planned schedule.

    SA Reference: SA 220, SA 300
    """

    _name = "general_audit_ws_c435bcd"
    _description = "Assignment Letter (c435bcd)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_assignment_letter." "worksheet_type_c435bcd"
    )
    _checklist_model_name = "general_audit_ws_c435bcd.checklist"
    _item_model_name = "general_audit_ws_c435bcd.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_c435bcd.checklist",
    )
