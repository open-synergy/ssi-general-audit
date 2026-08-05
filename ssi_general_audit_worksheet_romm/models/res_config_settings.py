# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    romm_scoring_config_id = fields.Many2one(
        string="Risk Configuration",
        comodel_name="general_audit_romm_scoring_config",
        config_parameter="ssi_general_audit_worksheet_romm.romm_scoring_config_id",
        help=(
            "Risk Configuration record used to compute the Account Level "
            "ROMM (weights/thresholds for ROMM Risk Initial and ROMM Risk "
            "Further). If left empty, the first available Risk "
            "Configuration record is used."
        ),
    )
