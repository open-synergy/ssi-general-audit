# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSf9a2c3d(models.Model):
    """Test of Detail Planning Worksheet (f9a2c3d).

    One worksheet per General Audit. It lists one line per standard
    account of the audit and records, for each of them, the planning of
    the Test of Detail: the account balance, the performance
    materiality, the assessed ROMM, the assertion types, the result of
    the analytical procedures and the timing, extent and primary audit
    techniques chosen by the auditor.

    The lines are loaded with ``action_load_detail`` (the **Detail**
    button) from the standard accounts of the audit and from the
    Specific Materiality and Analytical Procedures - Cycle worksheets.

    Reference standards: ISA 300, ISA 330, ISA 530.
    """

    _name = "general_audit_ws_f9a2c3d"
    _description = "Test of Detail Planning (f9a2c3d)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_test_planning.worksheet_type_f9a2c3d"

    detail_ids = fields.One2many(
        string="Details",
        comodel_name="general_audit_ws_f9a2c3d.detail",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
        help=(
            "One line per standard account of the General Audit. Columns "
            "up to AP Result are loaded automatically; Timing, Extent and "
            "Primary Audit Technique are filled in by the auditor."
        ),
    )

    def action_load_detail(self):
        """Synchronise ``detail_ids`` with the standard accounts.

        Triggers :meth:`_load_detail` (wrapped in ``sudo()``) for every
        record in the current recordset.

        :return: nothing; adds, removes and refreshes detail lines
        """
        for record in self.sudo():
            record._load_detail()

    def _load_detail(self):
        """Synchronise ``detail_ids`` with ``general_audit.standard_detail``.

        A line is created for each standard detail that belongs to
        ``general_audit_id`` and has none, and the lines of standard
        details that no longer match the criteria are removed. Other
        lines are kept as they are, so the Timing, Extent and Primary
        Audit Technique chosen by the auditor are never lost. The stored
        computed columns of the kept lines are refreshed, and pressing
        the button again without changes alters nothing.

        :return: nothing; adds, removes and refreshes detail lines
        """
        self.ensure_one()
        Detail = self.env["general_audit_ws_f9a2c3d.detail"]
        wanted = self.env["general_audit.standard_detail"].search(
            self._get_standard_detail_criteria()
        )
        obsolete = self.detail_ids.filtered(
            lambda line: line.standard_detail_id not in wanted
        )
        obsolete.unlink()
        kept = self.detail_ids - obsolete
        for standard_detail in wanted - kept.mapped("standard_detail_id"):
            Detail.create(
                {
                    "worksheet_id": self.id,
                    "standard_detail_id": standard_detail.id,
                }
            )
        kept._refresh_computed_columns()

    def _get_standard_detail_criteria(self):
        """Return the domain of the standard accounts to load.

        :return: a domain limited to the General Audit of the worksheet
        """
        self.ensure_one()
        return [("general_audit_id", "=", self.general_audit_id.id)]
