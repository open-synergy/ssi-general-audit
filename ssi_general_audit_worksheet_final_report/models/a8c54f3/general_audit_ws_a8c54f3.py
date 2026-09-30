# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models


class GeneralAuditWSa8c54f3(models.Model):
    """
    WS.090.1 — Audit Final Memorandum (a8c54f3)

    Documents the **audit final memorandum** — the engagement partner's
    formal summary at the close of fieldwork that brings together all key
    audit conclusions before the auditor's report is issued.  As required
    by ISA 220 / SA 220 (Quality Control for an Audit of Financial
    Statements) and ISA 700 / SA 700 (Forming an Opinion), the engagement
    partner must satisfy themselves that:

    - All significant risks and findings have been addressed.
    - The evidence obtained is sufficient and appropriate.
    - The conclusions on each significant area are reasonable and
      consistent with the financial statement as a whole.
    - The form of the auditor's report is appropriate.

    This worksheet captures the engagement partner's overall conclusion
    narrative and serves as the final sign-off document before issuing
    the auditor's report.

    Links to every Risk Response (RE) and Windup & Reporting (WR) working
    paper are exposed as ``link_1_id``..``link_48_id`` (RE first, ordered
    by ``general_audit_worksheet_type.sequence``, then WR in the same
    order). A worksheet type that allows more than one worksheet per
    audit (``allowed_audit=True``) is exposed as a Many2many
    ``link_N_ids`` listing every open/done worksheet; the other types
    stay Many2one ``link_N_id``, each paired with ``link_N_state``,
    ``link_N_conclusion_id`` and ``link_N_conclusion`` mirrored from
    the linked worksheet. ``action_reload_links`` recomputes all 48 on
    demand.

    **ISA / SA references:** ISA 220 / SA 220 — Quality Control for an
    Audit of Financial Statements; ISA 700 / SA 700 — Forming an Opinion
    and Reporting on Financial Statements
    """

    _name = "general_audit_ws_a8c54f3"
    _description = "Audit Final Memorandum (a8c54f3)"
    _inherit = [
        "general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_general_audit_worksheet_final_report." "worksheet_type_a8c54f3"

    proposed_audit_opinion_id = fields.Many2one(
        string="Proposed Audit Opinion",
        comodel_name="accountant.opinion",
        help="Audit opinion proposed by the engagement partner prior to "
        "issuing the final auditor's report.",
    )

    # General Ledger
    # LINK - 1 d209914
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_1_ids(self):
        """Populate ``link_1_ids`` with the open/done worksheets.

        Links every worksheet of type "General Ledger"
        (``general_audit_ws_d209914``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d209914"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_1_ids = obj.search(criteria)
            if link_1_ids:
                result = link_1_ids.ids
            record.link_1_ids = result

    link_1_ids = fields.Many2many(
        string="General Ledger",
        comodel_name="general_audit_ws_d209914",
        compute_sudo=True,
        compute="_compute_link_1_ids",
        store=True,
        help=(
            "Collection of all (General Ledger) worksheets linked to this "
            "General Audit. Automatically computed and stored."
        ),
    )

    # Subledger
    # LINK - 2 b5e3d9f
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_2_ids(self):
        """Populate ``link_2_ids`` with the open/done worksheets.

        Links every worksheet of type "Subledger"
        (``general_audit_ws_b5e3d9f``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b5e3d9f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_2_ids = obj.search(criteria)
            if link_2_ids:
                result = link_2_ids.ids
            record.link_2_ids = result

    link_2_ids = fields.Many2many(
        string="Subledger",
        comodel_name="general_audit_ws_b5e3d9f",
        compute_sudo=True,
        compute="_compute_link_2_ids",
        store=True,
        help=(
            "Collection of all (Subledger) worksheets linked to this "
            "General  Audit. Automatically computed and stored."
        ),
    )

    # Test of Control
    # LINK - 3 e3f4a5b
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_3_ids(self):
        """Populate ``link_3_ids`` with the open/done worksheets.

        Links every worksheet of type "Test of Control"
        (``general_audit_ws_e3f4a5b``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e3f4a5b"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_3_ids = obj.search(criteria)
            if link_3_ids:
                result = link_3_ids.ids
            record.link_3_ids = result

    link_3_ids = fields.Many2many(
        string="Test of Control",
        comodel_name="general_audit_ws_e3f4a5b",
        compute_sudo=True,
        compute="_compute_link_3_ids",
        store=True,
        help=(
            "Collection of all (Test of Control) worksheets linked to "
            "this  General Audit. Automatically computed and stored."
        ),
    )

    # Analytical Procedures - Cycle
    # LINK - 4 a3c9d2e
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_4_ids(self):
        """Populate ``link_4_ids`` with the open/done worksheets.

        Links every worksheet of type "Analytical Procedures - Cycle"
        (``general_audit_ws_a3c9d2e``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a3c9d2e"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_4_ids = obj.search(criteria)
            if link_4_ids:
                result = link_4_ids.ids
            record.link_4_ids = result

    link_4_ids = fields.Many2many(
        string="Analytical Procedures - Cycle",
        comodel_name="general_audit_ws_a3c9d2e",
        compute_sudo=True,
        compute="_compute_link_4_ids",
        store=True,
        help=(
            "Collection of all (Analytical Procedures - Cycle) worksheets "
            "linked to this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Key Audit Procedures
    # LINK - 5 e51bb1c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_5_ids(self):
        """Populate ``link_5_ids`` with the open/done worksheets.

        Links every worksheet of type "Key Audit Procedures"
        (``general_audit_ws_e51bb1c``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e51bb1c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_5_ids = obj.search(criteria)
            if link_5_ids:
                result = link_5_ids.ids
            record.link_5_ids = result

    link_5_ids = fields.Many2many(
        string="Key Audit Procedures",
        comodel_name="general_audit_ws_e51bb1c",
        compute_sudo=True,
        compute="_compute_link_5_ids",
        store=True,
        help=(
            "Collection of all (Key Audit Procedures) worksheets linked "
            "to this  General Audit. Automatically computed and stored."
        ),
    )

    # Test Planning
    # LINK - 6 f9a2c3d
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_6_ids(self):
        """Populate ``link_6_ids`` with the open/done worksheets.

        Links every worksheet of type "Test Planning"
        (``general_audit_ws_f9a2c3d``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f9a2c3d"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_6_ids = obj.search(criteria)
            if link_6_ids:
                result = link_6_ids.ids
            record.link_6_ids = result

    link_6_ids = fields.Many2many(
        string="Test Planning",
        comodel_name="general_audit_ws_f9a2c3d",
        compute_sudo=True,
        compute="_compute_link_6_ids",
        store=True,
        help=(
            "Collection of all (Test Planning) worksheets linked to this "
            "General Audit. Automatically computed and stored."
        ),
    )

    # Sample Determination
    # LINK - 7 a916660
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_7_ids(self):
        """Populate ``link_7_ids`` with the open/done worksheets.

        Links every worksheet of type "Sample Determination"
        (``general_audit_ws_a916660``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a916660"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_7_ids = obj.search(criteria)
            if link_7_ids:
                result = link_7_ids.ids
            record.link_7_ids = result

    link_7_ids = fields.Many2many(
        string="Sample Determination",
        comodel_name="general_audit_ws_a916660",
        compute_sudo=True,
        compute="_compute_link_7_ids",
        store=True,
        help=(
            "Collection of all (Sample Determination) worksheets linked "
            "to this  General Audit. Automatically computed and stored."
        ),
    )

    # Test of Detail
    # LINK - 8 b4f8e1a
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_8_ids(self):
        """Populate ``link_8_ids`` with the open/done worksheets.

        Links every worksheet of type "Test of Detail"
        (``general_audit_ws_b4f8e1a``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b4f8e1a"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_8_ids = obj.search(criteria)
            if link_8_ids:
                result = link_8_ids.ids
            record.link_8_ids = result

    link_8_ids = fields.Many2many(
        string="Test of Detail",
        comodel_name="general_audit_ws_b4f8e1a",
        compute_sudo=True,
        compute="_compute_link_8_ids",
        store=True,
        help=(
            "Collection of all (Test of Detail) worksheets linked to this "
            "General Audit. Automatically computed and stored."
        ),
    )

    # Vouching Audit Procedure
    # LINK - 9 b4f7d9c
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_9_ids(self):
        """Populate ``link_9_ids`` with the open/done worksheets.

        Links every worksheet of type "Vouching Audit Procedure"
        (``general_audit_ws_b4f7d9c``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b4f7d9c"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_9_ids = obj.search(criteria)
            if link_9_ids:
                result = link_9_ids.ids
            record.link_9_ids = result

    link_9_ids = fields.Many2many(
        string="Vouching Audit Procedure",
        comodel_name="general_audit_ws_b4f7d9c",
        compute_sudo=True,
        compute="_compute_link_9_ids",
        store=True,
        help=(
            "Collection of all (Vouching Audit Procedure) worksheets "
            "linked to  this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Physical Check
    # LINK - 10 c7d5f2b
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_10_ids(self):
        """Populate ``link_10_ids`` with the open/done worksheets.

        Links every worksheet of type "Physical Check"
        (``general_audit_ws_c7d5f2b``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c7d5f2b"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_10_ids = obj.search(criteria)
            if link_10_ids:
                result = link_10_ids.ids
            record.link_10_ids = result

    link_10_ids = fields.Many2many(
        string="Physical Check",
        comodel_name="general_audit_ws_c7d5f2b",
        compute_sudo=True,
        compute="_compute_link_10_ids",
        store=True,
        help=(
            "Collection of all (Physical Check) worksheets linked to this "
            "General Audit. Automatically computed and stored."
        ),
    )

    # Observation Audit Procedure
    # LINK - 11 d4d1ac0
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_11_ids(self):
        """Populate ``link_11_ids`` with the open/done worksheets.

        Links every worksheet of type "Observation Audit Procedure"
        (``general_audit_ws_d4d1ac0``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d4d1ac0"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_11_ids = obj.search(criteria)
            if link_11_ids:
                result = link_11_ids.ids
            record.link_11_ids = result

    link_11_ids = fields.Many2many(
        string="Observation Audit Procedure",
        comodel_name="general_audit_ws_d4d1ac0",
        compute_sudo=True,
        compute="_compute_link_11_ids",
        store=True,
        help=(
            "Collection of all (Observation Audit Procedure) worksheets "
            "linked  to this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Confirmation Audit Procedure
    # LINK - 12 d45dd19
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_12_ids(self):
        """Populate ``link_12_ids`` with the open/done worksheets.

        Links every worksheet of type "Confirmation Audit Procedure"
        (``general_audit_ws_d45dd19``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d45dd19"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_12_ids = obj.search(criteria)
            if link_12_ids:
                result = link_12_ids.ids
            record.link_12_ids = result

    link_12_ids = fields.Many2many(
        string="Confirmation Audit Procedure",
        comodel_name="general_audit_ws_d45dd19",
        compute_sudo=True,
        compute="_compute_link_12_ids",
        store=True,
        help=(
            "Collection of all (Confirmation Audit Procedure) worksheets "
            "linked  to this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Recompute Audit Procedure
    # LINK - 13 c6c86fd
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_13_ids(self):
        """Populate ``link_13_ids`` with the open/done worksheets.

        Links every worksheet of type "Recompute Audit Procedure"
        (``general_audit_ws_c6c86fd``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c6c86fd"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_13_ids = obj.search(criteria)
            if link_13_ids:
                result = link_13_ids.ids
            record.link_13_ids = result

    link_13_ids = fields.Many2many(
        string="Recompute Audit Procedure",
        comodel_name="general_audit_ws_c6c86fd",
        compute_sudo=True,
        compute="_compute_link_13_ids",
        store=True,
        help=(
            "Collection of all (Recompute Audit Procedure) worksheets "
            "linked to  this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Reperformance Audit Procedure
    # LINK - 14 d1ecfb7
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_14_ids(self):
        """Populate ``link_14_ids`` with the open/done worksheets.

        Links every worksheet of type "Reperformance Audit Procedure"
        (``general_audit_ws_d1ecfb7``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d1ecfb7"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_14_ids = obj.search(criteria)
            if link_14_ids:
                result = link_14_ids.ids
            record.link_14_ids = result

    link_14_ids = fields.Many2many(
        string="Reperformance Audit Procedure",
        comodel_name="general_audit_ws_d1ecfb7",
        compute_sudo=True,
        compute="_compute_link_14_ids",
        store=True,
        help=(
            "Collection of all (Reperformance Audit Procedure) worksheets "
            "linked to this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Plausible Relationship Audit Procedure
    # LINK - 15 aa899baf
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_15_ids(self):
        """Populate ``link_15_ids`` with the open/done worksheets.

        Links every worksheet of type "Plausible Relationship Audit Procedure"
        (``general_audit_ws_aa899baf``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_aa899baf"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_15_ids = obj.search(criteria)
            if link_15_ids:
                result = link_15_ids.ids
            record.link_15_ids = result

    link_15_ids = fields.Many2many(
        string="Plausible Relationship Audit Procedure",
        comodel_name="general_audit_ws_aa899baf",
        compute_sudo=True,
        compute="_compute_link_15_ids",
        store=True,
        help=(
            "Collection of all (Plausible Relationship Audit Procedure) "
            "worksheets linked to this General Audit. Automatically "
            "computed  and stored."
        ),
    )

    # Comparative Audit Procedure
    # LINK - 16 de3244b
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_16_ids(self):
        """Populate ``link_16_ids`` with the open/done worksheets.

        Links every worksheet of type "Comparative Audit Procedure"
        (``general_audit_ws_de3244b``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_de3244b"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_16_ids = obj.search(criteria)
            if link_16_ids:
                result = link_16_ids.ids
            record.link_16_ids = result

    link_16_ids = fields.Many2many(
        string="Comparative Audit Procedure",
        comodel_name="general_audit_ws_de3244b",
        compute_sudo=True,
        compute="_compute_link_16_ids",
        store=True,
        help=(
            "Collection of all (Comparative Audit Procedure) worksheets "
            "linked  to this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Inquiry Audit Procedures
    # LINK - 17 a145276
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_17_ids(self):
        """Populate ``link_17_ids`` with the open/done worksheets.

        Links every worksheet of type "Inquiry Audit Procedures"
        (``general_audit_ws_a145276``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a145276"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_17_ids = obj.search(criteria)
            if link_17_ids:
                result = link_17_ids.ids
            record.link_17_ids = result

    link_17_ids = fields.Many2many(
        string="Inquiry Audit Procedures",
        comodel_name="general_audit_ws_a145276",
        compute_sudo=True,
        compute="_compute_link_17_ids",
        store=True,
        help=(
            "Collection of all (Inquiry Audit Procedures) worksheets "
            "linked to  this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Accounting Estimation
    # LINK - 18 a8f4d88
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_18_id(self):
        """Populate ``link_18_id`` from open/done Accounting Estimation
        worksheets.

        Searches ``general_audit_ws_a8f4d88`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a8f4d88"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_18_id = obj.search(criteria, limit=1)
            if link_18_id:
                result = link_18_id.id
            record.link_18_id = result

    link_18_id = fields.Many2one(
        string="Accounting Estimation",
        comodel_name="general_audit_ws_a8f4d88",
        compute_sudo=True,
        compute="_compute_link_18_id",
        store=True,
        help=(
            "Link to worksheet (Accounting Estimation) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_18_state = fields.Selection(
        string="State",
        related="link_18_id.state",
        help=(
            "Workflow state of the linked Accounting Estimation worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_18_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_18_id.conclusion_id",
        help=(
            "Conclusion from the Accounting Estimation worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_18_conclusion = fields.Text(
        string="Conclusion",
        related="link_18_id.conclusion",
        help=(
            "Conclusion on the Accounting Estimation worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Related Party Transaction
    # LINK - 19 c40cfd9
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_19_id(self):
        """Populate ``link_19_id`` from open/done Related Party Transaction
        worksheets.

        Searches ``general_audit_ws_c40cfd9`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c40cfd9"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_19_id = obj.search(criteria, limit=1)
            if link_19_id:
                result = link_19_id.id
            record.link_19_id = result

    link_19_id = fields.Many2one(
        string="Related Party Transaction",
        comodel_name="general_audit_ws_c40cfd9",
        compute_sudo=True,
        compute="_compute_link_19_id",
        store=True,
        help=(
            "Link to worksheet (Related Party Transaction) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_19_state = fields.Selection(
        string="State",
        related="link_19_id.state",
        help=(
            "Workflow state of the linked Related Party Transaction "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_19_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_19_id.conclusion_id",
        help=(
            "Conclusion from the Related Party Transaction worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_19_conclusion = fields.Text(
        string="Conclusion",
        related="link_19_id.conclusion",
        help=(
            "Conclusion on the Related Party Transaction worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Subsequent Event
    # LINK - 20 cb82c5f
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_20_id(self):
        """Populate ``link_20_id`` from open/done Subsequent Event worksheets.

        Searches ``general_audit_ws_cb82c5f`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_cb82c5f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_20_id = obj.search(criteria, limit=1)
            if link_20_id:
                result = link_20_id.id
            record.link_20_id = result

    link_20_id = fields.Many2one(
        string="Subsequent Event",
        comodel_name="general_audit_ws_cb82c5f",
        compute_sudo=True,
        compute="_compute_link_20_id",
        store=True,
        help=(
            "Link to worksheet (Subsequent Event) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_20_state = fields.Selection(
        string="State",
        related="link_20_id.state",
        help=(
            "Workflow state of the linked Subsequent Event worksheet. Read- "
            "only and follows the linked record."
        ),
    )
    link_20_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_20_id.conclusion_id",
        help=(
            "Conclusion from the Subsequent Event worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_20_conclusion = fields.Text(
        string="Conclusion",
        related="link_20_id.conclusion",
        help=(
            "Conclusion on the Subsequent Event worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )

    # Going Concern
    # LINK - 21 fbf57ee
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_21_id(self):
        """Populate ``link_21_id`` from open/done Going Concern worksheets.

        Searches ``general_audit_ws_fbf57ee`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_fbf57ee"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_21_id = obj.search(criteria, limit=1)
            if link_21_id:
                result = link_21_id.id
            record.link_21_id = result

    link_21_id = fields.Many2one(
        string="Going Concern",
        comodel_name="general_audit_ws_fbf57ee",
        compute_sudo=True,
        compute="_compute_link_21_id",
        store=True,
        help=(
            "Link to worksheet (Going Concern) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_21_state = fields.Selection(
        string="State",
        related="link_21_id.state",
        help=(
            "Workflow state of the linked Going Concern worksheet. Read-only "
            "and follows the linked record."
        ),
    )
    link_21_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_21_id.conclusion_id",
        help=(
            "Conclusion from the Going Concern worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )
    link_21_conclusion = fields.Text(
        string="Conclusion",
        related="link_21_id.conclusion",
        help=(
            "Conclusion on the Going Concern worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )

    # Auditor Expert
    # LINK - 22 bab9d32
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_22_ids(self):
        """Populate ``link_22_ids`` with the open/done worksheets.

        Links every worksheet of type "Auditor Expert"
        (``general_audit_ws_bab9d32``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bab9d32"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_22_ids = obj.search(criteria)
            if link_22_ids:
                result = link_22_ids.ids
            record.link_22_ids = result

    link_22_ids = fields.Many2many(
        string="Auditor Expert",
        comodel_name="general_audit_ws_bab9d32",
        compute_sudo=True,
        compute="_compute_link_22_ids",
        store=True,
        help=(
            "Collection of all (Auditor Expert) worksheets linked to this "
            "General Audit. Automatically computed and stored."
        ),
    )

    # Management Expert
    # LINK - 23 cda3a68
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_23_ids(self):
        """Populate ``link_23_ids`` with the open/done worksheets.

        Links every worksheet of type "Management Expert"
        (``general_audit_ws_cda3a68``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_cda3a68"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_23_ids = obj.search(criteria)
            if link_23_ids:
                result = link_23_ids.ids
            record.link_23_ids = result

    link_23_ids = fields.Many2many(
        string="Management Expert",
        comodel_name="general_audit_ws_cda3a68",
        compute_sudo=True,
        compute="_compute_link_23_ids",
        store=True,
        help=(
            "Collection of all (Management Expert) worksheets linked to "
            "this  General Audit. Automatically computed and stored."
        ),
    )

    # Commitment and Contingent
    # LINK - 24 ee819ae
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_24_id(self):
        """Populate ``link_24_id`` from open/done Commitment and Contingent
        worksheets.

        Searches ``general_audit_ws_ee819ae`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ee819ae"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_24_id = obj.search(criteria, limit=1)
            if link_24_id:
                result = link_24_id.id
            record.link_24_id = result

    link_24_id = fields.Many2one(
        string="Commitment and Contingent",
        comodel_name="general_audit_ws_ee819ae",
        compute_sudo=True,
        compute="_compute_link_24_id",
        store=True,
        help=(
            "Link to worksheet (Commitment and Contingent) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_24_state = fields.Selection(
        string="State",
        related="link_24_id.state",
        help=(
            "Workflow state of the linked Commitment and Contingent "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_24_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_24_id.conclusion_id",
        help=(
            "Conclusion from the Commitment and Contingent worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_24_conclusion = fields.Text(
        string="Conclusion",
        related="link_24_id.conclusion",
        help=(
            "Conclusion on the Commitment and Contingent worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Lead Schedule - Account
    # LINK - 25 f9f3299
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_25_ids(self):
        """Populate ``link_25_ids`` with the open/done worksheets.

        Links every worksheet of type "Lead Schedule - Account"
        (``general_audit_ws_f9f3299``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f9f3299"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_25_ids = obj.search(criteria)
            if link_25_ids:
                result = link_25_ids.ids
            record.link_25_ids = result

    link_25_ids = fields.Many2many(
        string="Lead Schedule - Account",
        comodel_name="general_audit_ws_f9f3299",
        compute_sudo=True,
        compute="_compute_link_25_ids",
        store=True,
        help=(
            "Collection of all (Lead Schedule - Account) worksheets "
            "linked to  this General Audit. Automatically computed and "
            "stored."
        ),
    )

    # Worksheet
    # LINK - 26 b26d482
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_26_id(self):
        """Populate ``link_26_id`` from open/done Worksheet worksheets.

        Searches ``general_audit_ws_b26d482`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b26d482"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_26_id = obj.search(criteria, limit=1)
            if link_26_id:
                result = link_26_id.id
            record.link_26_id = result

    link_26_id = fields.Many2one(
        string="Worksheet",
        comodel_name="general_audit_ws_b26d482",
        compute_sudo=True,
        compute="_compute_link_26_id",
        store=True,
        help=(
            "Link to worksheet (Worksheet) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_26_state = fields.Selection(
        string="State",
        related="link_26_id.state",
        help=(
            "Workflow state of the linked Worksheet worksheet. Read-only and "
            "follows the linked record."
        ),
    )
    link_26_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_26_id.conclusion_id",
        help=(
            "Conclusion from the Worksheet worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )
    link_26_conclusion = fields.Text(
        string="Conclusion",
        related="link_26_id.conclusion",
        help=(
            "Conclusion on the Worksheet worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )

    # Population
    # LINK - 27 a01723b
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_27_ids(self):
        """Populate ``link_27_ids`` with the open/done worksheets.

        Links every worksheet of type "Population"
        (``general_audit_ws_a01723b``) that shares the same
        ``general_audit_id`` and has ``state`` in
        ``["open", "done"]``. Every match is linked: the worksheet
        type allows more than one per audit
        (``allowed_audit=True``).
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a01723b"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_27_ids = obj.search(criteria)
            if link_27_ids:
                result = link_27_ids.ids
            record.link_27_ids = result

    link_27_ids = fields.Many2many(
        string="Population",
        comodel_name="general_audit_ws_a01723b",
        compute_sudo=True,
        compute="_compute_link_27_ids",
        store=True,
        help=(
            "Collection of all (Population) worksheets linked to this "
            "General  Audit. Automatically computed and stored."
        ),
    )

    # Audit Result Formulation
    # LINK - 28 ab19fd4
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_28_id(self):
        """Populate ``link_28_id`` from open/done Audit Result Formulation
        worksheets.

        Searches ``general_audit_ws_ab19fd4`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ab19fd4"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_28_id = obj.search(criteria, limit=1)
            if link_28_id:
                result = link_28_id.id
            record.link_28_id = result

    link_28_id = fields.Many2one(
        string="Audit Result Formulation",
        comodel_name="general_audit_ws_ab19fd4",
        compute_sudo=True,
        compute="_compute_link_28_id",
        store=True,
        help=(
            "Link to worksheet (Audit Result Formulation) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_28_state = fields.Selection(
        string="State",
        related="link_28_id.state",
        help=(
            "Workflow state of the linked Audit Result Formulation worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_28_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_28_id.conclusion_id",
        help=(
            "Conclusion from the Audit Result Formulation worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_28_conclusion = fields.Text(
        string="Conclusion",
        related="link_28_id.conclusion",
        help=(
            "Conclusion on the Audit Result Formulation worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Findings That Influence Opinion
    # LINK - 29 a0319a2
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_29_id(self):
        """Populate ``link_29_id`` from open/done Findings That Influence
        Opinion worksheets.

        Searches ``general_audit_ws_a0319a2`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_a0319a2"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_29_id = obj.search(criteria, limit=1)
            if link_29_id:
                result = link_29_id.id
            record.link_29_id = result

    link_29_id = fields.Many2one(
        string="Findings That Influence Opinion",
        comodel_name="general_audit_ws_a0319a2",
        compute_sudo=True,
        compute="_compute_link_29_id",
        store=True,
        help=(
            "Link to worksheet (Findings That Influence Opinion) for this "
            "General Audit. Automatically computed and stored."
        ),
    )
    link_29_state = fields.Selection(
        string="State",
        related="link_29_id.state",
        help=(
            "Workflow state of the linked Findings That Influence Opinion "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_29_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_29_id.conclusion_id",
        help=(
            "Conclusion from the Findings That Influence Opinion worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )
    link_29_conclusion = fields.Text(
        string="Conclusion",
        related="link_29_id.conclusion",
        help=(
            "Conclusion on the Findings That Influence Opinion worksheet. "
            "Read-only, mirrors the linked record."
        ),
    )

    # Control Deficiencies
    # LINK - 30 d33420f
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_30_id(self):
        """Populate ``link_30_id`` from open/done Control Deficiencies
        worksheets.

        Searches ``general_audit_ws_d33420f`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_d33420f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_30_id = obj.search(criteria, limit=1)
            if link_30_id:
                result = link_30_id.id
            record.link_30_id = result

    link_30_id = fields.Many2one(
        string="Control Deficiencies",
        comodel_name="general_audit_ws_d33420f",
        compute_sudo=True,
        compute="_compute_link_30_id",
        store=True,
        help=(
            "Link to worksheet (Control Deficiencies) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_30_state = fields.Selection(
        string="State",
        related="link_30_id.state",
        help=(
            "Workflow state of the linked Control Deficiencies worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_30_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_30_id.conclusion_id",
        help=(
            "Conclusion from the Control Deficiencies worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_30_conclusion = fields.Text(
        string="Conclusion",
        related="link_30_id.conclusion",
        help=(
            "Conclusion on the Control Deficiencies worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Audit Result Discussion
    # LINK - 31 bc3e272
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_31_id(self):
        """Populate ``link_31_id`` from open/done Audit Result Discussion
        worksheets.

        Searches ``general_audit_ws_bc3e272`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bc3e272"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_31_id = obj.search(criteria, limit=1)
            if link_31_id:
                result = link_31_id.id
            record.link_31_id = result

    link_31_id = fields.Many2one(
        string="Audit Result Discussion",
        comodel_name="general_audit_ws_bc3e272",
        compute_sudo=True,
        compute="_compute_link_31_id",
        store=True,
        help=(
            "Link to worksheet (Audit Result Discussion) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_31_state = fields.Selection(
        string="State",
        related="link_31_id.state",
        help=(
            "Workflow state of the linked Audit Result Discussion worksheet. "
            "Read-only and follows the linked record."
        ),
    )
    link_31_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_31_id.conclusion_id",
        help=(
            "Conclusion from the Audit Result Discussion worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_31_conclusion = fields.Text(
        string="Conclusion",
        related="link_31_id.conclusion",
        help=(
            "Conclusion on the Audit Result Discussion worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Final Materiality
    # LINK - 32 bb33b94
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_32_id(self):
        """Populate ``link_32_id`` from open/done Final Materiality worksheets.

        Searches ``general_audit_ws_bb33b94`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bb33b94"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_32_id = obj.search(criteria, limit=1)
            if link_32_id:
                result = link_32_id.id
            record.link_32_id = result

    link_32_id = fields.Many2one(
        string="Final Materiality",
        comodel_name="general_audit_ws_bb33b94",
        compute_sudo=True,
        compute="_compute_link_32_id",
        store=True,
        help=(
            "Link to worksheet (Final Materiality) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_32_state = fields.Selection(
        string="State",
        related="link_32_id.state",
        help=(
            "Workflow state of the linked Final Materiality worksheet. Read- "
            "only and follows the linked record."
        ),
    )
    link_32_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_32_id.conclusion_id",
        help=(
            "Conclusion from the Final Materiality worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_32_conclusion = fields.Text(
        string="Conclusion",
        related="link_32_id.conclusion",
        help=(
            "Conclusion on the Final Materiality worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Final Analytical Procedures
    # LINK - 33 c2375d8
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_33_id(self):
        """Populate ``link_33_id`` from open/done Final Analytical Procedures
        worksheets.

        Searches ``general_audit_ws_c2375d8`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_c2375d8"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_33_id = obj.search(criteria, limit=1)
            if link_33_id:
                result = link_33_id.id
            record.link_33_id = result

    link_33_id = fields.Many2one(
        string="Final Analytical Procedures",
        comodel_name="general_audit_ws_c2375d8",
        compute_sudo=True,
        compute="_compute_link_33_id",
        store=True,
        help=(
            "Link to worksheet (Final Analytical Procedures) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_33_state = fields.Selection(
        string="State",
        related="link_33_id.state",
        help=(
            "Workflow state of the linked Final Analytical Procedures "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_33_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_33_id.conclusion_id",
        help=(
            "Conclusion from the Final Analytical Procedures worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_33_conclusion = fields.Text(
        string="Conclusion",
        related="link_33_id.conclusion",
        help=(
            "Conclusion on the Final Analytical Procedures worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Final Analytical Procedures - Vertical and Horizontal Analysis
    # LINK - 34 e1f2d98
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_34_id(self):
        """Populate ``link_34_id`` from open/done Final Analytical Procedures -
        Vertical and Horizontal Analysis worksheets.

        Searches ``general_audit_ws_e1f2d98`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e1f2d98"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_34_id = obj.search(criteria, limit=1)
            if link_34_id:
                result = link_34_id.id
            record.link_34_id = result

    link_34_id = fields.Many2one(
        string=("Final Analytical Procedures - Vertical and Horizontal Analysis"),
        comodel_name="general_audit_ws_e1f2d98",
        compute_sudo=True,
        compute="_compute_link_34_id",
        store=True,
        help=(
            "Link to worksheet (Final Analytical Procedures - Vertical and "
            "Horizontal Analysis) for this General Audit. Automatically "
            "computed and stored."
        ),
    )
    link_34_state = fields.Selection(
        string="State",
        related="link_34_id.state",
        help=(
            "Workflow state of the linked Final Analytical Procedures - "
            "Vertical and Horizontal Analysis worksheet. Read-only and "
            "follows the linked record."
        ),
    )
    link_34_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_34_id.conclusion_id",
        help=(
            "Conclusion from the Final Analytical Procedures - Vertical and "
            "Horizontal Analysis worksheet. Read-only, mirrors the linked "
            "record."
        ),
    )
    link_34_conclusion = fields.Text(
        string="Conclusion",
        related="link_34_id.conclusion",
        help=(
            "Conclusion on the Final Analytical Procedures - Vertical and "
            "Horizontal Analysis worksheet. Read-only, mirrors the linked "
            "record."
        ),
    )

    # Final Analytical Procedures - Ratio Analysis
    # LINK - 35 f3a78de
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_35_id(self):
        """Populate ``link_35_id`` from open/done Final Analytical Procedures -
        Ratio Analysis worksheets.

        Searches ``general_audit_ws_f3a78de`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_f3a78de"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_35_id = obj.search(criteria, limit=1)
            if link_35_id:
                result = link_35_id.id
            record.link_35_id = result

    link_35_id = fields.Many2one(
        string="Final Analytical Procedures - Ratio Analysis",
        comodel_name="general_audit_ws_f3a78de",
        compute_sudo=True,
        compute="_compute_link_35_id",
        store=True,
        help=(
            "Link to worksheet (Final Analytical Procedures - Ratio Analysis) "
            "for this General Audit. Automatically computed and stored."
        ),
    )
    link_35_state = fields.Selection(
        string="State",
        related="link_35_id.state",
        help=(
            "Workflow state of the linked Final Analytical Procedures - Ratio "
            "Analysis worksheet. Read-only and follows the linked record."
        ),
    )
    link_35_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_35_id.conclusion_id",
        help=(
            "Conclusion from the Final Analytical Procedures - Ratio Analysis "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )
    link_35_conclusion = fields.Text(
        string="Conclusion",
        related="link_35_id.conclusion",
        help=(
            "Conclusion on the Final Analytical Procedures - Ratio Analysis "
            "worksheet. Read-only, mirrors the linked record."
        ),
    )

    # Report Formatting Control
    # LINK - 36 b555edd
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_36_id(self):
        """Populate ``link_36_id`` from open/done Report Formatting Control
        worksheets.

        Searches ``general_audit_ws_b555edd`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b555edd"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_36_id = obj.search(criteria, limit=1)
            if link_36_id:
                result = link_36_id.id
            record.link_36_id = result

    link_36_id = fields.Many2one(
        string="Report Formatting Control",
        comodel_name="general_audit_ws_b555edd",
        compute_sudo=True,
        compute="_compute_link_36_id",
        store=True,
        help=(
            "Link to worksheet (Report Formatting Control) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_36_state = fields.Selection(
        string="State",
        related="link_36_id.state",
        help=(
            "Workflow state of the linked Report Formatting Control "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_36_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_36_id.conclusion_id",
        help=(
            "Conclusion from the Report Formatting Control worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_36_conclusion = fields.Text(
        string="Conclusion",
        related="link_36_id.conclusion",
        help=(
            "Conclusion on the Report Formatting Control worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Draft Financial Statements
    # LINK - 37 e59c663
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_37_id(self):
        """Populate ``link_37_id`` from open/done Draft Financial Statements
        worksheets.

        Searches ``general_audit_ws_e59c663`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_e59c663"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_37_id = obj.search(criteria, limit=1)
            if link_37_id:
                result = link_37_id.id
            record.link_37_id = result

    link_37_id = fields.Many2one(
        string="Draft Financial Statements",
        comodel_name="general_audit_ws_e59c663",
        compute_sudo=True,
        compute="_compute_link_37_id",
        store=True,
        help=(
            "Link to worksheet (Draft Financial Statements) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_37_state = fields.Selection(
        string="State",
        related="link_37_id.state",
        help=(
            "Workflow state of the linked Draft Financial Statements "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_37_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_37_id.conclusion_id",
        help=(
            "Conclusion from the Draft Financial Statements worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_37_conclusion = fields.Text(
        string="Conclusion",
        related="link_37_id.conclusion",
        help=(
            "Conclusion on the Draft Financial Statements worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Final Discussion
    # LINK - 38 de69c2f
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_38_id(self):
        """Populate ``link_38_id`` from open/done Final Discussion worksheets.

        Searches ``general_audit_ws_de69c2f`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_de69c2f"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_38_id = obj.search(criteria, limit=1)
            if link_38_id:
                result = link_38_id.id
            record.link_38_id = result

    link_38_id = fields.Many2one(
        string="Final Discussion",
        comodel_name="general_audit_ws_de69c2f",
        compute_sudo=True,
        compute="_compute_link_38_id",
        store=True,
        help=(
            "Link to worksheet (Final Discussion) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_38_state = fields.Selection(
        string="State",
        related="link_38_id.state",
        help=(
            "Workflow state of the linked Final Discussion worksheet. Read- "
            "only and follows the linked record."
        ),
    )
    link_38_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_38_id.conclusion_id",
        help=(
            "Conclusion from the Final Discussion worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_38_conclusion = fields.Text(
        string="Conclusion",
        related="link_38_id.conclusion",
        help=(
            "Conclusion on the Final Discussion worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )

    # Audit Result
    # LINK - 39 ff42fdc
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_39_id(self):
        """Populate ``link_39_id`` from open/done Audit Result worksheets.

        Searches ``general_audit_ws_ff42fdc`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ff42fdc"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_39_id = obj.search(criteria, limit=1)
            if link_39_id:
                result = link_39_id.id
            record.link_39_id = result

    link_39_id = fields.Many2one(
        string="Audit Result",
        comodel_name="general_audit_ws_ff42fdc",
        compute_sudo=True,
        compute="_compute_link_39_id",
        store=True,
        help=(
            "Link to worksheet (Audit Result) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_39_state = fields.Selection(
        string="State",
        related="link_39_id.state",
        help=(
            "Workflow state of the linked Audit Result worksheet. Read-only "
            "and follows the linked record."
        ),
    )
    link_39_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_39_id.conclusion_id",
        help=(
            "Conclusion from the Audit Result worksheet. Read-only, mirrors "
            "the linked record."
        ),
    )
    link_39_conclusion = fields.Text(
        string="Conclusion",
        related="link_39_id.conclusion",
        help=(
            "Conclusion on the Audit Result worksheet. Read-only, mirrors the "
            "linked record."
        ),
    )

    # Management Letter
    # LINK - 40 ae598e6
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_40_id(self):
        """Populate ``link_40_id`` from open/done Management Letter worksheets.

        Searches ``general_audit_ws_ae598e6`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_ae598e6"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_40_id = obj.search(criteria, limit=1)
            if link_40_id:
                result = link_40_id.id
            record.link_40_id = result

    link_40_id = fields.Many2one(
        string="Management Letter",
        comodel_name="general_audit_ws_ae598e6",
        compute_sudo=True,
        compute="_compute_link_40_id",
        store=True,
        help=(
            "Link to worksheet (Management Letter) for this General Audit. "
            "Automatically computed and stored."
        ),
    )
    link_40_state = fields.Selection(
        string="State",
        related="link_40_id.state",
        help=(
            "Workflow state of the linked Management Letter worksheet. Read- "
            "only and follows the linked record."
        ),
    )
    link_40_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_40_id.conclusion_id",
        help=(
            "Conclusion from the Management Letter worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )
    link_40_conclusion = fields.Text(
        string="Conclusion",
        related="link_40_id.conclusion",
        help=(
            "Conclusion on the Management Letter worksheet. Read-only, "
            "mirrors the linked record."
        ),
    )

    # Management Representation
    # LINK - 41 bbbdfe7
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_41_id(self):
        """Populate ``link_41_id`` from open/done Management Representation
        worksheets.

        Searches ``general_audit_ws_bbbdfe7`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_bbbdfe7"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_41_id = obj.search(criteria, limit=1)
            if link_41_id:
                result = link_41_id.id
            record.link_41_id = result

    link_41_id = fields.Many2one(
        string="Management Representation",
        comodel_name="general_audit_ws_bbbdfe7",
        compute_sudo=True,
        compute="_compute_link_41_id",
        store=True,
        help=(
            "Link to worksheet (Management Representation) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_41_state = fields.Selection(
        string="State",
        related="link_41_id.state",
        help=(
            "Workflow state of the linked Management Representation "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_41_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_41_id.conclusion_id",
        help=(
            "Conclusion from the Management Representation worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_41_conclusion = fields.Text(
        string="Conclusion",
        related="link_41_id.conclusion",
        help=(
            "Conclusion on the Management Representation worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    # Independent Auditor Report
    # LINK - 48 b66777d
    @api.depends(
        "general_audit_id",
    )
    def _compute_link_48_id(self):
        """Populate ``link_48_id`` from open/done Independent Auditor Report
        worksheets.

        Searches ``general_audit_ws_b66777d`` records sharing the same
        ``general_audit_id`` with ``state`` in ``["open", "done"]``, plus
        ``limit=1``: like other worksheet types, more than one open/done record
        may exist per audit, so the first match by default order is used
        instead of raising on multiple results.
        """
        for record in self:
            result = False
            obj = self.env["general_audit_ws_b66777d"]
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("state", "in", ["open", "done"]),
            ]
            link_48_id = obj.search(criteria, limit=1)
            if link_48_id:
                result = link_48_id.id
            record.link_48_id = result

    link_48_id = fields.Many2one(
        string="Independent Auditor Report",
        comodel_name="general_audit_ws_b66777d",
        compute_sudo=True,
        compute="_compute_link_48_id",
        store=True,
        help=(
            "Link to worksheet (Independent Auditor Report) for this General "
            "Audit. Automatically computed and stored."
        ),
    )
    link_48_state = fields.Selection(
        string="State",
        related="link_48_id.state",
        help=(
            "Workflow state of the linked Independent Auditor Report "
            "worksheet. Read-only and follows the linked record."
        ),
    )
    link_48_conclusion_id = fields.Many2one(
        string="Conclusion ID",
        related="link_48_id.conclusion_id",
        help=(
            "Conclusion from the Independent Auditor Report worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )
    link_48_conclusion = fields.Text(
        string="Conclusion",
        related="link_48_id.conclusion",
        help=(
            "Conclusion on the Independent Auditor Report worksheet. Read- "
            "only, mirrors the linked record."
        ),
    )

    def action_reload_links(self):
        """Recompute every Link field (``link_N_id`` and ``link_N_ids``).

        Callable from the form view so the engagement partner can refresh
        the RE/WR working-paper links after upstream worksheets change
        state, without reloading the whole record.

        :return: ``None``.
        """
        for record in self.sudo():
            record._reload_links()

    def _reload_links(self):
        """Force-recompute every ``link_N_id``/``link_N_ids`` on ``self``.

        Extension point: called by ``action_reload_links``; kept separate
        so a glue module can override it to also refresh fields it adds.

        :return: ``None``.
        """
        self.ensure_one()
        self._compute_link_1_ids()
        self._compute_link_2_ids()
        self._compute_link_3_ids()
        self._compute_link_4_ids()
        self._compute_link_5_ids()
        self._compute_link_6_ids()
        self._compute_link_7_ids()
        self._compute_link_8_ids()
        self._compute_link_9_ids()
        self._compute_link_10_ids()
        self._compute_link_11_ids()
        self._compute_link_12_ids()
        self._compute_link_13_ids()
        self._compute_link_14_ids()
        self._compute_link_15_ids()
        self._compute_link_16_ids()
        self._compute_link_17_ids()
        self._compute_link_18_id()
        self._compute_link_19_id()
        self._compute_link_20_id()
        self._compute_link_21_id()
        self._compute_link_22_ids()
        self._compute_link_23_ids()
        self._compute_link_24_id()
        self._compute_link_25_ids()
        self._compute_link_26_id()
        self._compute_link_27_ids()
        self._compute_link_28_id()
        self._compute_link_29_id()
        self._compute_link_30_id()
        self._compute_link_31_id()
        self._compute_link_32_id()
        self._compute_link_33_id()
        self._compute_link_34_id()
        self._compute_link_35_id()
        self._compute_link_36_id()
        self._compute_link_37_id()
        self._compute_link_38_id()
        self._compute_link_39_id()
        self._compute_link_40_id()
        self._compute_link_41_id()
        # link_42..link_47 (review-owned models: be62e79, a025441, bcc0d76,
        # dae9f3c, cae598e, fc75636) are added by an extension of this
        # method in ssi_general_audit_worksheet_review (which already
        # depends on this module) -- see that module's a8c54f3 extension.
        self._compute_link_48_id()

    def _get_custom_field_labels(self):
        """Map each Link field to its KKA (working paper) display name.

        :return: dict of ``{field_name: label}`` for every ``link_N_id``
            and ``link_N_ids``, used wherever the generic field label is not
            descriptive enough (e.g. audit report annexures).
        """
        return {
            "link_1_ids": _("General Ledger"),
            "link_2_ids": _("Subledger"),
            "link_3_ids": _("Test of Control"),
            "link_4_ids": _("Analytical Procedures - Cycle"),
            "link_5_ids": _("Key Audit Procedures"),
            "link_6_ids": _("Test Planning"),
            "link_7_ids": _("Sample Determination"),
            "link_8_ids": _("Test of Detail"),
            "link_9_ids": _("Vouching Audit Procedure"),
            "link_10_ids": _("Physical Check"),
            "link_11_ids": _("Observation Audit Procedure"),
            "link_12_ids": _("Confirmation Audit Procedure"),
            "link_13_ids": _("Recompute Audit Procedure"),
            "link_14_ids": _("Reperformance Audit Procedure"),
            "link_15_ids": _("Plausible Relationship Audit Procedure"),
            "link_16_ids": _("Comparative Audit Procedure"),
            "link_17_ids": _("Inquiry Audit Procedures"),
            "link_18_id": _("Accounting Estimation"),
            "link_19_id": _("Related Party Transaction"),
            "link_20_id": _("Subsequent Event"),
            "link_21_id": _("Going Concern"),
            "link_22_ids": _("Auditor Expert"),
            "link_23_ids": _("Management Expert"),
            "link_24_id": _("Commitment and Contingent"),
            "link_25_ids": _("Lead Schedule - Account"),
            "link_26_id": _("Worksheet"),
            "link_27_ids": _("Population"),
            "link_28_id": _("Audit Result Formulation"),
            "link_29_id": _("Findings That Influence Opinion"),
            "link_30_id": _("Control Deficiencies"),
            "link_31_id": _("Audit Result Discussion"),
            "link_32_id": _("Final Materiality"),
            "link_33_id": _("Final Analytical Procedures"),
            "link_34_id": _(
                "Final Analytical Procedures - Vertical and Horizontal " "Analysis"
            ),
            "link_35_id": _("Final Analytical Procedures - Ratio Analysis"),
            "link_36_id": _("Report Formatting Control"),
            "link_37_id": _("Draft Financial Statements"),
            "link_38_id": _("Final Discussion"),
            "link_39_id": _("Audit Result"),
            "link_40_id": _("Management Letter"),
            "link_41_id": _("Management Representation"),
            # link_42..link_47 labels are added by the extension in
            # ssi_general_audit_worksheet_review (see _reload_links above).
            "link_48_id": _("Independent Auditor Report"),
        }
