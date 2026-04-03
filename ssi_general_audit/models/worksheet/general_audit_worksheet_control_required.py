# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models, tools


class GeneralAuditWorksheetControlRequired(models.Model):
    """
    Tipe Worksheet Wajib per Audit (SQL View).

    View read-only yang memuat seluruh tipe worksheet yang bersifat wajib
    (``required = True``) bagi sebuah dokumen general audit. Data diambil
    dari konfigurasi ``general_audit_worksheet_type`` yang ditandai sebagai
    wajib pada engagement audit tertentu. Digunakan sebagai subset dari
    ``general_audit.worksheet_control`` untuk memisahkan worksheet wajib
    dari worksheet tambahan.
    """

    _name = "general_audit.worksheet_control_required"
    _description = "Accountant General Audit Required Worksheet Control"
    _auto = False

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        help="General Audit that requires this worksheet type.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="general_audit_worksheet_type",
        ondelete="restrict",
        help="Required worksheet type configured for the audit.",
    )
    required = fields.Boolean(
        string="Required",
        help="Always True for required worksheet types.",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.id AS general_audit_id,
            b.worksheet_type_id AS type_id,
            True AS required
        """
        return select_str

    def _from(self):
        from_str = """
        general_audit AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN rel_general_audit_2_required_worksheet_type AS b ON a.id = b.general_audit_id
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
