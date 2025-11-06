# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import _, api, models
from odoo.exceptions import ValidationError


class GeneralAudit(models.Model):
    _name = "general_audit"
    _inherit = ["general_audit"]

    @api.constrains("accountant_id")
    def _check_num_of_cpa(self):
        for record in self.sudo():
            num_of_cp = len(
                self.read_group(
                    domain=[], fields=["accountant_id"], groupby=["accountant_id"]
                )
            )
            max_allowed_cp = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ssi_general_audit.max_number_of_cpa_license", default="0")
            )
            if num_of_cp > int(max_allowed_cp):
                error_message = _(
                    "❌ Failed to create a new record.\n\n"
                    "⚙️ Context:\n"
                    "\t• Document Type: %s\n"
                    "\t• Record ID : %s\n\n"
                    "⚠️ Problem :\n"
                    "\t Max number of CPA License exceeded. : \n"
                    "\t\t• Current: %s.\n"
                    "\t\t• Allowed: %s.\n\n"
                    "💡 Recommended Action:\n"
                    "\tContact us to increase the limit."
                ) % (
                    self._description.lower(),
                    record.id,
                    num_of_cp,
                    max_allowed_cp,
                )
                raise ValidationError(error_message)
