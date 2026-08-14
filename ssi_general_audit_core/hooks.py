# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
import logging

from odoo import SUPERUSER_ID, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Set the main company's default currency and country.

    Some CI/dev pipelines pre-install a chart of accounts before this
    module, which can create journal items in another currency and make
    ``res.company.write`` on ``currency_id`` raise (Odoo refuses to
    change a company's currency once journal items already exist).
    Best-effort: keep the company's existing currency instead of
    failing the whole module installation in that case.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    company = env.ref("base.main_company")
    try:
        company.write(
            {
                "currency_id": env.ref("base.IDR").id,
                "country_id": env.ref("base.id").id,
            }
        )
    except UserError:
        _logger.warning(
            "Skipping default currency setup for %s: currency could not "
            "be changed (journal items already exist).",
            company.display_name,
        )
