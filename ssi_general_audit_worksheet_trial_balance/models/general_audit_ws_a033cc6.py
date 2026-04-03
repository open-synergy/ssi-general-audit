# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa033cc6(models.Model):
    """Worksheet: Trial Balance (a033cc6).

    The trial balance worksheet is a foundational audit working paper that
    forms the bridge between the client's accounting records and the financial
    statements subject to audit. It is used during the execution phase of the
    audit to verify and document that:

    - The client's trial balance agrees in total to the general ledger
    - Opening balances are consistent with the prior period's closing balances
    - Proposed audit adjustments are tracked and reflected
    - The adjusted trial balance ties to the audited financial statements

    This worksheet is based on general audit standards for documentation and
    working paper requirements (ISA 230 / SA 230 — Audit Documentation) and
    supports substantive procedures performed across all account areas.

    Checklist items in this worksheet are configurable via master items and
    represent verification checkpoints that auditors must complete before
    finalising the trial balance as a base for further audit work.

    Inherits from:
    - ``general_audit_worksheet_mixin``: standard audit worksheet lifecycle
      (state machine, sequence, audit link, approval)
    - ``mixin.checklist``: checklist item population from master item list
    """

    _name = "general_audit_ws_a033cc6"
    _description = "Trial Balance (a033cc6)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_trial_balance." "worksheet_type_a033cc6"
    _checklist_model_name = "general_audit_ws_a033cc6.checklist"
    _item_model_name = "general_audit_ws_a033cc6.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_a033cc6.checklist",
        help=(
            "Collection of checklist items for this trial balance worksheet. "
            "Each checklist item represents a specific audit verification point "
            "related to trial balance accuracy and completeness."
        ),
    )
