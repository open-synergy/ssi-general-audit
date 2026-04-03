# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditExpertType(models.Model):
    """Master: Expert Type.

    Reference list of expert specialisation types that may be engaged during
    an audit (e.g., valuation expert, actuary, legal counsel, IT specialist,
    geologist). Per ISA 620 / SA 620, auditors must evaluate expert competence
    and objectivity. This master is used in the Main Business Activity worksheet
    (ae11f7e) to classify and track experts used on the engagement.
    """

    _name = "general_audit_expert_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Expert Type"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
