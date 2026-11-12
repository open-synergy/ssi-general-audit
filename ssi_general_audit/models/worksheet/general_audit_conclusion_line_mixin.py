# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditConclusionLineMixin(models.AbstractModel):
    """Conclusion summary of one worksheet type inside a memorandum.

    Concrete models inherit this mixin and add the Many2one that points to
    the owning memorandum. One line summarises every open or done worksheet
    of ``type_id`` that belongs to the same General Audit. When exactly one
    worksheet exists the summary mirrors its conclusion and is locked in the
    view. When several exist the summary is typed by the user and survives
    every reload.
    """

    _name = "general_audit_conclusion_line_mixin"
    _description = "General Audit Conclusion Line Mixin"
    _order = "type_sequence, id"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
        help="General Audit whose worksheets are summarised by this line.",
    )
    type_id = fields.Many2one(
        string="Worksheet Type",
        comodel_name="general_audit_worksheet_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        help="Worksheet type summarised by this line.",
    )
    type_sequence = fields.Integer(
        string="Type Sequence",
        related="type_id.sequence",
        store=True,
        compute_sudo=True,
        help="Sequence of the worksheet type. Used to order the lines.",
    )

    @api.depends(
        "general_audit_id",
        "type_id",
    )
    def _compute_worksheet_ids(self):
        """Collect the open or done worksheets summarised by this line.

        Searches ``general_audit_worksheet`` records of the same General
        Audit whose ``parent_type_id`` equals ``type_id``. The result is not
        stored, so ``_refresh_conclusion`` recomputes it on reload.
        """
        Worksheet = self.env["general_audit_worksheet"]
        for record in self:
            result = []
            if record.general_audit_id and record.type_id:
                criteria = record._get_worksheet_criteria()
                result = Worksheet.search(criteria).ids
            record.worksheet_ids = result

    worksheet_ids = fields.Many2many(
        string="Worksheets",
        comodel_name="general_audit_worksheet",
        compute="_compute_worksheet_ids",
        store=False,
        compute_sudo=True,
        help="Open or done worksheets of this type in the same audit.",
    )

    @api.depends("worksheet_ids")
    def _compute_worksheet_count(self):
        """Count the worksheets summarised by this line."""
        for record in self:
            result = len(record.worksheet_ids)
            record.worksheet_count = result
            record.locked_ok = result < 2

    worksheet_count = fields.Integer(
        string="Number of Worksheets",
        compute="_compute_worksheet_count",
        store=False,
        compute_sudo=True,
        help="Number of open or done worksheets of this type.",
    )
    locked_ok = fields.Boolean(
        string="Summary Locked",
        compute="_compute_worksheet_count",
        store=False,
        compute_sudo=True,
        help="Checked when fewer than two worksheets exist: the summary then "
        "follows the worksheet and cannot be edited.",
    )

    @api.depends("worksheet_ids", "worksheet_ids.conclusion")
    def _compute_conclusion(self):
        """Mirror the worksheet conclusion when only one worksheet exists.

        With exactly one worksheet the value is taken from it. When more
        worksheets exist, a value that still equals the conclusion of one
        of them is a leftover mirror and is cleared so that the user writes
        a summary of all worksheets. Any other text is typed by the user
        and is kept.
        """
        for record in self:
            result = record.conclusion
            worksheets = record.worksheet_ids
            if len(worksheets) == 1:
                result = worksheets.conclusion
            elif len(worksheets) > 1 and result in worksheets.mapped("conclusion"):
                result = False
            record.conclusion = result

    conclusion = fields.Text(
        string="Conclusion Summary",
        compute="_compute_conclusion",
        store=True,
        readonly=False,
        compute_sudo=True,
        help="Summary of the conclusions of the worksheets of this type. "
        "Follows the worksheet when only one exists, otherwise typed by hand. "
        "A copied conclusion is cleared when a second worksheet appears.",
    )

    def _get_worksheet_criteria(self):
        """Return the domain that selects the summarised worksheets.

        Extension point: override to change which worksheets are summarised.

        :return: domain for ``general_audit_worksheet``
        """
        self.ensure_one()
        return [
            ("general_audit_id", "=", self.general_audit_id.id),
            ("parent_type_id", "=", self.type_id.id),
            ("state", "in", ["open", "done"]),
        ]

    def _refresh_conclusion(self):
        """Recompute the worksheets and the summary of these lines.

        ``worksheet_ids`` depends only on the audit and the type, so a new
        worksheet does not trigger it. Reload Links calls this method to pick
        new worksheets up.
        """
        self.invalidate_cache(["worksheet_ids", "worksheet_count", "locked_ok"])
        self._compute_worksheet_ids()
        self._compute_worksheet_count()
        self._compute_conclusion()
