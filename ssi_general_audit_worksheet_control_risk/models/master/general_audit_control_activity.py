# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditControlActivity(models.Model):
    """Master data — control activity classification.

    References a type of control activity as defined in the COSO or ISA
    framework (e.g., Authorisation, Reconciliation, Physical Safeguard,
    Segregation of Duties, IT Controls).  Used to classify key internal
    controls in the ``general_audit_key_internal_control`` master.
    """

    _name = "general_audit_control_activity"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Control Activity"
