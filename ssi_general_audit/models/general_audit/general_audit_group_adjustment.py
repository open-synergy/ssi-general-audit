# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models, tools


class GeneralAuditGroupAdjustment(models.Model):
    _name = "general_audit.group_adjustment"
    _description = "Accountant General Audit Group Adjustment"
    _auto = False

    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="client_account_group",
        ondelete="restrict",
        help="Account group affected by adjustments.",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        ondelete="cascade",
        help="General Audit document related to the group adjustment summary.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        compute_sudo=True,
        store=False,
        help="Currency used for displaying debit and credit amounts.",
    )
    debit = fields.Monetary(
        string="Debit",
        currency_field="currency_id",
        help="Total debits from adjustment entries aggregated by group.",
    )
    credit = fields.Monetary(
        string="Credit",
        currency_field="currency_id",
        help="Total credits from adjustment entries aggregated by group.",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            b.general_audit_id AS general_audit_id,
            d.group_id AS group_id,
            SUM(a.debit) AS debit,
            SUM(a.credit) AS credit
        """
        return select_str

    def _from(self):
        from_str = """
        client_adjustment_entry_detail AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN client_adjustment_entry AS b ON a.entry_id = b.id
        JOIN client_account AS c ON a.account_id = c.id
        JOIN client_account_type AS d ON c.type_id = d.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    b.general_audit_id,
                    d.group_id
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
