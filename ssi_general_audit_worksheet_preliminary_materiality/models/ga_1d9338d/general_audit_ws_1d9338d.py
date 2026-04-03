# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWS1d9338d(models.Model):
    """
    WS: Preliminary Materiality Checklist (1d9338d) — ISA 320 / SA 320.

    A structured Yes / No / N-A checklist that confirms the auditor has
    followed the prescribed steps for establishing and documenting materiality.

    Checklist item types (``checklist_type``):

    * ``materiality_comp``   — Confirms that the materiality computation
      process (base amount selection, percentage determination, OM/PM/TM
      calculation) has been properly performed and documented.
    * ``account_mapping``    — Confirms that all significant accounts have
      been assessed against materiality thresholds and that material
      accounts have been identified for additional audit focus.
    """

    _name = "general_audit_ws_1d9338d"
    _description = "Preliminary Materiality (1d9338d)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_preliminary_materiality." "worksheet_type_1d9338d"
    )
    _checklist_model_name = "general_audit_ws_1d9338d.checklist"
    _item_model_name = "general_audit_ws_1d9338d.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_1d9338d.checklist",
        help="Checklist lines associated with this worksheet.",
    )
