# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class GeneralAuditWSb9d8a5cIndependencyItem(models.Model):
    """Master data: Independence impairment factor for engagement team assessment.

    Defines a specific independence threat or impairment circumstance used
    in the independency analysis section of the ``general_audit_ws_b9d8a5c``
    worksheet. Inherits ``mixin.master_data``.

    Examples of items include: direct financial interests in the client,
    family relationships with client management, recent employment by the
    client, and advocacy or self-review threats as defined in the IAPI
    Code of Ethics and ISQC 1.

    Model: ``general_audit_ws_b9d8a5c.independency_item``
    SA Reference: SA 220, ISQC 1
    """

    _name = "general_audit_ws_b9d8a5c.independency_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = (
        "independency, Availability and Independency "
        "Of Assignment Team (b9d8a5c) - independency Item"
    )

    code = fields.Char(
        default="/",
    )
