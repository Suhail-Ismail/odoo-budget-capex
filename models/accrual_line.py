# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class AccrualLine(models.Model):
    _name = 'budget.capex.accrual.line'
    _description = 'Cear Accrual Line'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    physical_progress = fields.Float(string='Pysical Progress (%)',
                                     digits=(5, 2),
                                     help='Progress in terms of work completion in percentage (ie. 60% progress)')
    milestone = fields.Char()
    amount = fields.Monetary(string='Acrual Amount',
                             currency_field='currency_id')
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    accrual_id = fields.Many2one('budget.capex.accrual',
                                 string='Accrual')
    cear_id = fields.Many2one('budget.capex.cear',
                              string='Cear No')
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    # CONSTRAINS
    # ----------------------------------------------------------
