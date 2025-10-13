# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Executed once after module installation."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    ta_computation_item_id = (
        "ssi_general_audit." "trial_balance_computation_item_1_d0b0cb3e"
    )
    tr_computation_item_id = (
        "ssi_general_audit." "trial_balance_computation_item_5_2a8e8641"
    )

    try:
        ta_item = env.ref(ta_computation_item_id, raise_if_not_found=False)
        tr_item = env.ref(tr_computation_item_id, raise_if_not_found=False)
    except ValueError:
        ta_item = tr_item = False

    if not (ta_item or tr_item):
        return

    companies = env["res.company"].search([])
    for company in companies:
        vals = {}
        if ta_item:
            vals["ta_computation_item_id"] = ta_item.id
        if tr_item:
            vals["tr_computation_item_id"] = tr_item.id
        if vals:
            company.write(vals)
