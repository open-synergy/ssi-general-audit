# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import fields, models


class TeamRole(models.Model):
    """
    Peran dalam Tim Audit (Team Role).

    Master data yang mendefinisikan peran-peran anggota tim audit dalam
    satu engagement general audit (mis. Engagement Partner / Rekan
    Penanggungjawab, Manager, Senior Auditor, Junior Auditor). Digunakan
    untuk mendokumentasikan susunan tim dan tanggung jawab masing-masing
    anggota sesuai ISQC 1 / SQCS dan SA 220 (Quality Control for an
    Audit of Financial Statements).
    """

    _name = "team_role"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Roles in the team"

    code = fields.Char(
        default="/",
        help="Unique short code for the team role. Use '/' to auto-generate.",
    )
