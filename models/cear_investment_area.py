# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class BudgetInvestmentArea(models.Model):
    _name = 'budget.capex.cear.investment.area'
    _rec_name = 'name'

    name = fields.Char(string="Name")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    cear_ids = fields.One2many('budget.capex.cear',
                               'investment_area_id',
                               string="Cears")
