# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditRelevantRegulation(models.Model):
    """
    Regulasi / Standar Akuntansi yang Relevan.

    Master data yang merepresentasikan regulasi, standar akuntansi, atau
    peraturan perundangan yang relevan terhadap entitas yang diaudit
    (mis. PSAK, ISAK, UU Perseroan Terbatas, peraturan OJK). Digunakan
    dalam pemahaman entitas dan lingkungannya sesuai ISA 315 / SA 315.
    Setiap regulasi dapat memiliki butir-butir detail melalui ``item_ids``.
    """

    _name = "general_audit_relevant_regulation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Relevant Regulation"

    item_ids = fields.One2many(
        string="Regulation Items",
        comodel_name="general_audit_relevant_regulation.item",
        inverse_name="regulation_id",
        help="List of detailed items under this regulation.",
    )
