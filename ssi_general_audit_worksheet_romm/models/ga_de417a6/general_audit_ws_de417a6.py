# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde417a6(models.Model):
    """
    WS: ROMM Checklist (de417a6) — ISA 315 / SA 315.

    A structured Yes / No / N-A checklist that confirms all required risk
    assessment procedures prescribed by ISA 315 have been completed and
    documented, including:

    * Understanding of the entity and its environment has been sufficiently
      obtained.
    * Significant risks have been identified and a planned response has
      been documented for each.
    * Account-level and assertion-level ROMM has been assessed for all
      material accounts.
    * Financial statement-level risks and responses have been documented.
    * ROMM assessment has been communicated to the audit team.
    """

    _name = "general_audit_ws_de417a6"
    _description = "ROMM (de417a6)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_romm." "worksheet_type_de417a6"
    _checklist_model_name = "general_audit_ws_de417a6.checklist"
    _item_model_name = "general_audit_ws_de417a6.item"

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de417a6.checklist",
        help=(
            "Checklist responses for this worksheet. Each line stores the answer to a "
            "defined checklist item."
        ),
    )
