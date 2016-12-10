# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class BudgetInvestmentArea(models.Model):
    _name = 'budget.capex.task.investment.area'
    _rec_name = 'name'

    name = fields.Char(string="Name")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    task_ids = fields.One2many('budget.capex.task',
                               'task_investment_area_id',
                               string="Tasks")
