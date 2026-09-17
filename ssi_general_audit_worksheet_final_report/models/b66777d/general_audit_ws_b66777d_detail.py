# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.misc import get_lang
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditWsB66777dDetail(models.Model):
    """One row of the "Details" summary table on WS.090.2 (b66777d).

    Stores a single Property / Python Code / Value line. The 11 fixed
    rows are (re)populated by ``general_audit_ws_b66777d.
    action_populate_detail()`` -- a full unlink-then-recreate snapshot
    of the linked General Audit at the moment it is clicked, not a
    live-reactive summary and not auto-filled on worksheet creation
    (see that method's docstring).

    Not exposed for manual editing: every group's
    create/write/unlink permission on this model is 0 in
    ``security/ir.model.access.csv``, so only the ``sudo()``-wrapped
    populate logic inside ``general_audit_ws_b66777d._populate_detail()``
    can write to it.
    """

    _name = "general_audit_ws_b66777d.detail"
    _description = "Independent Auditor Report (b66777d) - Details"

    worksheet_id = fields.Many2one(
        string="Worksheet",
        comodel_name="general_audit_ws_b66777d",
        required=True,
        ondelete="cascade",
        help=("Independent Auditor's Report worksheet this Details row " "belongs to."),
    )
    property_id = fields.Many2one(
        string="Property",
        comodel_name="general_audit_ws_b66777d.property",
        required=True,
        ondelete="restrict",
        help=(
            "Master data row (Configuration > ... > Independent "
            "Auditor Report > Detail Property) this Details row was "
            "populated from."
        ),
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        help=(
            "Python snippet evaluated on every Populate click to "
            "derive this row's Value. COPIED from property_id.python_"
            "code at populate time (not related=), so editing the "
            "master data afterwards does not change a row already "
            "snapshotted -- consistent with Populate being a manual, "
            "point-in-time action rather than a live-reactive one. "
            "Available names: 'env' and 'document' (this detail "
            "record itself)."
        ),
    )
    value = fields.Char(
        string="Value",
        readonly=True,
        compute="_compute_value",
        store=True,
        compute_sudo=True,
        help=(
            "Result of python_code, always as a display-ready string: "
            "text results are used as-is, numeric results are "
            "thousand-separator formatted (see _compute_value)."
        ),
    )

    def _get_localdict(self):
        """Build the ``safe_eval`` namespace for ``python_code``.

        Same shape as ``general_audit.computation._get_extrapolation_
        localdict``: only ``env`` and ``document`` (this record) are
        exposed to the snippet.

        :return: localdict for safe_eval
        :rtype: dict
        """
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.depends(
        "python_code",
    )
    def _compute_value(self):
        """Evaluate ``python_code`` into the display-ready ``value``.

        Depending only on ``python_code`` (set once per row, at the
        moment ``general_audit_ws_b66777d._populate_detail()``
        unlinks and recreates every row) is deliberate: it makes this
        compute fire exactly once per row's lifetime, matching the
        "snapshot on Populate, not live" design in the issue's
        Keputusan Desain, without needing a separate flag to suppress
        recomputation.

        ``python_code`` is executed with ``safe_eval(mode="exec",
        nocopy=True)``, the same mechanism as
        ``general_audit.computation._recompute_audited``. Any
        exception during evaluation is swallowed and the row falls
        back to an empty ``value`` rather than blocking ``_populate_
        detail()`` -- a malformed or overly defensive snippet must
        never stop the Populate button from finishing.

        The evaluated ``result`` is coerced to a string:

        - already a ``str`` -- used as-is.
        - a non-boolean ``int``/``float`` -- thousand-separator
          formatted via ``get_lang(self.env).format(fmt, result,
          grouping=True, monetary=True)``, the same helper used by
          ``ssi_custom_information_mixin``'s own
          ``custom_info_value._compute_value`` for its numeric
          properties -- 0 decimals for ``int``, 2 for ``float``.
        - anything else falsy, or the ``except`` branch -- ``""``.

        :return: None
        """
        for record in self:
            value = ""
            try:
                localdict = record._get_localdict()
                eval(
                    record.python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
                if isinstance(result, str):
                    value = result
                elif isinstance(result, (int, float)) and not isinstance(result, bool):
                    lang = get_lang(record.env)
                    fmt = "%.0f" if isinstance(result, int) else "%.2f"
                    value = lang.format(fmt, result, grouping=True, monetary=True)
                elif result:
                    value = str(result)
            except Exception:
                pass
            record.value = value
