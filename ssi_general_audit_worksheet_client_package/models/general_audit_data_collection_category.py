# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class GeneralAuditDataCollectionCategory(models.Model):
    """Master: Data Collection Category.

    Groups the Data Collection master records so the items requested from
    the client can be classified (for example by the kind of document).
    """

    _name = "general_audit_data_collection_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit - Data Collection Category"
