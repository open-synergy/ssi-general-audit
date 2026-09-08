# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSde69c2f(models.Model):
    """Worksheet — Final Discussion (de69c2f).

    A checklist-driven worksheet guiding the engagement team through the
    final pre-issuance quality review before the audit report is signed.  Each
    checklist item (``checklist_ids``) represents a required step or check that
    must be completed and documented before the opinion can be issued.

    Typical items include: confirming all open points are resolved, verifying
    the completeness of the audit file, reviewing subsequent events through
    the report date, confirming management representations are obtained, and
    obtaining partner approval sign-off.

    Also cross-references the other Windup & Reporting KKAs of the same
    engagement -- Audit Result (``audit_result_id``), Management Letter
    (``management_letter_id``), and Management Representation
    (``management_representation_id``) -- each filled in on demand by its
    own Reload button (``action_reload_audit_result``,
    ``action_reload_management_letter``,
    ``action_reload_management_representation``) rather than kept in sync
    automatically.

    Workflow: Draft → Open → Confirm → Done
    ISA/SA references: ISA 560/SA 560 (Subsequent Events);
    ISA 700/SA 700 (Forming an Opinion);
    ISA 220/SA 220 (Quality Control for an Audit).
    """

    _name = "general_audit_ws_de69c2f"
    _description = "Final Discussion (de69c2f)"
    _inherit = [
        "general_audit_worksheet_mixin",
        "mixin.checklist",
    ]
    _type_xml_id = (
        "ssi_general_audit_worksheet_draft_reporting." "worksheet_type_de69c2f"
    )
    _checklist_model_name = "general_audit_ws_de69c2f.checklist"
    _item_model_name = "general_audit_ws_de69c2f.item"
    _checklist_create_page = False

    checklist_ids = fields.One2many(
        string="Checklist",
        comodel_name="general_audit_ws_de69c2f.checklist",
        help="Checklist lines for this worksheet.",
    )
    audit_result_id = fields.Many2one(
        string="# Audit Result",
        comodel_name="general_audit_ws_ff42fdc",
        ondelete="restrict",
        readonly=True,
        copy=False,
        help="Reference to the Audit Result (ff42fdc) worksheet of the "
        "same General Audit. Filled in by the Reload button on the "
        "Audit Result tab; not editable directly.",
    )
    management_letter_id = fields.Many2one(
        string="# Management Letter",
        comodel_name="general_audit_ws_ae598e6",
        ondelete="restrict",
        readonly=True,
        copy=False,
        help="Reference to the Management Letter (ae598e6) worksheet of "
        "the same General Audit. Filled in by the Reload button on the "
        "Management Letter tab; not editable directly.",
    )
    management_representation_id = fields.Many2one(
        string="# Management Representation",
        comodel_name="general_audit_ws_bbbdfe7",
        ondelete="restrict",
        readonly=True,
        copy=False,
        help="Reference to the Management Representation (bbbdfe7) "
        "worksheet of the same General Audit. Filled in by the Reload "
        "button on the Management Representation tab; not editable "
        "directly.",
    )

    def action_reload_audit_result(self):
        """Reload the Audit Result worksheet reference.

        Calls ``_reload_audit_result`` on every record in ``self``, run
        with ``sudo()`` so users without direct write access on
        ``general_audit_ws_ff42fdc`` can still trigger the reload from
        the button.
        """
        for record in self.sudo():
            record._reload_audit_result()

    def _reload_audit_result(self):
        """Synchronise ``audit_result_id`` with the sibling worksheet.

        Searches for the ``general_audit_ws_ff42fdc`` worksheet that
        shares this record's ``general_audit_id`` and writes its id to
        ``audit_result_id``. If no such sibling exists (yet), the field
        is set/kept ``False`` -- no error is raised.
        """
        self.ensure_one()
        found = self.env["general_audit_ws_ff42fdc"].search(
            [("general_audit_id", "=", self.general_audit_id.id)],
            limit=1,
        )
        self.write({"audit_result_id": found.id if found else False})

    def action_reload_management_letter(self):
        """Reload the Management Letter worksheet reference.

        Calls ``_reload_management_letter`` on every record in ``self``,
        run with ``sudo()`` so users without direct write access on
        ``general_audit_ws_ae598e6`` can still trigger the reload from
        the button.
        """
        for record in self.sudo():
            record._reload_management_letter()

    def _reload_management_letter(self):
        """Synchronise ``management_letter_id`` with sibling worksheet.

        Searches for the ``general_audit_ws_ae598e6`` worksheet that
        shares this record's ``general_audit_id`` and writes its id to
        ``management_letter_id``. If no such sibling exists (yet), the
        field is set/kept ``False`` -- no error is raised.
        """
        self.ensure_one()
        found = self.env["general_audit_ws_ae598e6"].search(
            [("general_audit_id", "=", self.general_audit_id.id)],
            limit=1,
        )
        self.write({"management_letter_id": found.id if found else False})

    def action_reload_management_representation(self):
        """Reload the Management Representation worksheet reference.

        Calls ``_reload_management_representation`` on every record in
        ``self``, run with ``sudo()`` so users without direct write
        access on ``general_audit_ws_bbbdfe7`` can still trigger the
        reload from the button.
        """
        for record in self.sudo():
            record._reload_management_representation()

    def _reload_management_representation(self):
        """Synchronise ``management_representation_id`` with sibling.

        Searches for the ``general_audit_ws_bbbdfe7`` worksheet that
        shares this record's ``general_audit_id`` and writes its id to
        ``management_representation_id``. If no such sibling exists
        (yet), the field is set/kept ``False`` -- no error is raised.
        """
        self.ensure_one()
        found = self.env["general_audit_ws_bbbdfe7"].search(
            [("general_audit_id", "=", self.general_audit_id.id)],
            limit=1,
        )
        self.write({"management_representation_id": (found.id if found else False)})
