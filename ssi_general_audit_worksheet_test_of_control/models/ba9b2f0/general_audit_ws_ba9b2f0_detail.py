# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class GeneralAuditWSba9b2f0Detail(models.Model):
    _name = "general_audit_ws_ba9b2f0.detail"
    _inherit = "general_audit_ws_ba9b2f0.detail"

    toc_attribute_id = fields.Many2one(
        string="ToC Attribute",
        comodel_name="general_audit_ws_e3f4a5b.attribute",
        ondelete="restrict",
        help=(
            "Test of Control attribute this control key relies on; "
            "ToC Analysis and ToC Reference are pulled from this link."
        ),
    )
    toc_analysis = fields.Selection(
        related="toc_attribute_id.conclusion",
        selection=[
            ("effective", "Effective"),
            ("not_effective", "Not Effective"),
        ],
        store=True,
        readonly=True,
        required=False,
        help="Assessment result pulled directly from the linked Test of Control attribute.",
    )
    toc_reference = fields.Many2one(
        string="ToC Reference",
        comodel_name="general_audit_ws_e3f4a5b",
        related="toc_attribute_id.worksheet_id",
        store=True,
        readonly=True,
        help="Test of Control worksheet linked via the selected attribute; clickable.",
    )

    @api.onchange("rely_on_control")
    def onchange_rely_on_control(self):
        """Clear the ToC link when the control is no longer relied upon.

        ``toc_analysis``/``toc_reference`` cascade-clear on their own since
        they are ``related`` to ``toc_attribute_id``.
        """
        if self.rely_on_control != "yes":
            self.toc_attribute_id = False

    def write(self, vals):
        """Force-clear ``toc_attribute_id`` when ``rely_on_control`` leaves "yes".

        ``toc_attribute_id`` is ``attrs``-readonly in the view whenever
        ``rely_on_control != "yes"``. Odoo's web client drops fields that are
        readonly in the record's *final* state from the write payload
        entirely - so the moment "Rely on Control" is switched to "No", the
        onchange-computed clear-to-False for ``toc_attribute_id`` (and the
        related ``toc_analysis``/``toc_reference`` that depend on it) is
        silently discarded on save and the old link reappears. Enforcing the
        clear here, independent of what the client actually sends, is the
        only way it survives the round trip.
        """
        if vals.get("rely_on_control") not in (None, "yes"):
            vals = dict(vals, toc_attribute_id=False)
        return super().write(vals)
