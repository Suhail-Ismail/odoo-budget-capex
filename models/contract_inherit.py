# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import num_to_shorthand


class Contract(models.Model):
    _inherit = 'budget.contractor.contract'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    cear_ids = fields.Many2many('budget.capex.cear',
                                'budget_cear_cear_contract',
                                'contract_id',
                                'cear_id',
                                string='CEARs')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # currency_id exist in the main contract model
