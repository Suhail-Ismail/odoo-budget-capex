# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .utils import choices_tuple

class Accrual(models.Model):
    _name = 'budget.accrual'
    _rec_name = 'acrual_no'
    _description = 'Accrual'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_capex = fields.Boolean(string='Is Capex')
    acrual_no = fields.Char(string="CWIP No", required=True)
    amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Amount')
    date = fields.Date(string="Accrual Date")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
