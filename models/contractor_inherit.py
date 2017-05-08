# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contractor(models.Model):
    _inherit = 'budget.contractor.contractor'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    cear_ids = fields.Many2many('budget.capex.cear',
                                'budget_cear_cear_contractor',
                                'contractor_id',
                                'cear_id',
                                string='CEARs')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
