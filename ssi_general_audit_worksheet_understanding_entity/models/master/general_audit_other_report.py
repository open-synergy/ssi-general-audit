# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditOtherReport(models.Model):
    """Master: Other Report Type.

    Reference list of other reports relevant to the audit engagement (e.g.,
    internal audit reports, management letters, regulatory examination reports,
    tax audit reports, sustainability reports). Used in the General Audit record
    to document other reports reviewed by the auditor as part of understanding
    the entity per ISA 315 and ISA 265.
    """

    _name = "general_audit_other_report"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Other Report"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
