# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models


class GeneralAuditStandardDetail(models.Model):
    """
    Extension of ``general_audit.standard_detail`` with ROMM assessment fields.

    This inheritance adds **Risk of Material Misstatement (ROMM)** assessment
    fields to each standard detail record, enabling the Account Level ROMM
    worksheet (``general_audit_ws_d66d87a``) to capture assertion-level risk
    evaluations directly on the detail.

    Added fields:

    * ``pr_assersion_type_ids`` — Presentation & Disclosure (P&D) assertion
      types applicable to this account (in addition to transaction-level
      assertions already on the base model).
    * ``romm`` — Overall assessed ROMM level: Low / Medium / High.
    * ``planned_response_analytic_procedure`` — Flag: analytical procedures
      planned in response to identified ROMM.
    * ``planned_response_toc`` — Flag: tests of controls (ToC) planned.
    * ``planned_response_tod`` — Flag: tests of detail (ToD) planned.
    * ``planned_response_interim`` — Flag: procedures planned for interim
      period (before year-end).
    """

    _name = "general_audit.standard_detail"
    _inherit = ["general_audit.standard_detail"]

    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        comodel_name="general_audit_assersion_type",
        relation="rel_standard_detail_2_pr_assersion_type",
        column1="standard_detail_id",
        column2="assersion_type_id",
        help=(
            "Presentation & Disclosure (P&D) assertion types applicable to this "
            "standard detail. Select all assertions relevant to the account or balance."
        ),
    )
    romm = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        help=(
            "Assessed risk of material misstatement (ROMM) for this standard detail "
            "at the assertion level. Choose Low, Medium, or High."
        ),
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
        help=(
            "Tick if analytical procedures are planned as a response to the identified "
            "ROMM for this assertion."
        ),
    )
    planned_response_toc = fields.Boolean(
        string="Planned Response ToC",
        default=False,
        help=(
            "Tick if tests of controls (ToC) are planned as a response to the identified ROMM."
        ),
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
        help=(
            "Tick if tests of details (ToD) are planned as a response to the identified ROMM."
        ),
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
        help=(
            "Indicates that the planned audit response will be performed during the "
            "interim period."
        ),
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
        help=(
            "Indicates that the planned audit response will be performed at year-end."
        ),
    )
