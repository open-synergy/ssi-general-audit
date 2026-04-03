# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSd33420f(models.Model):
    """Worksheet WR.110.2 — Control Deficiencies.

    Documents internal control deficiencies identified during the audit.
    Under ISA 265 / SA 265, the auditor is required to communicate significant
    deficiencies in writing to those charged with governance (TCWG), and other
    deficiencies to management where appropriate.

    A deficiency exists when a control is designed, implemented, or operated
    in a way that does not prevent, or detect-and-correct, misstatements in
    the financial statements on a timely basis.  This worksheet captures each
    deficiency in the 5-C format (Condition, Criteria, Cause, Effect,
    Recommendation) with a risk severity classification (major / minor).

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 265/SA 265 (Communicating Deficiencies in Internal
    Control); ISA 315/SA 315 (Identifying and Assessing the Risks).
    """

    _name = "general_audit_ws_d33420f"
    _description = "Control Deficiencies (d33420f)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_audit_result." "worksheet_type_d33420f"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_d33420f.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [("readonly", False)],
        },
        help=(
            "List of control deficiency detail lines captured in this worksheet. "
            "Editable when the worksheet is in the 'Open' state."
        ),
    )
