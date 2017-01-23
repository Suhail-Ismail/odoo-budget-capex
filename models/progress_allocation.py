# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_core.models.utilities import choices_tuple


class ProgressAllocation(models.Model):
    _name = 'budget.capex.progress.allocation'
    _rec_name = 'name'
    _description = 'Cear Progress Allocation'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string='Name')
    allocated_amount = fields.Monetary(string='Allocated Amount',
                                       currency_field='company_currency_id',
                                       store=True)
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    cear_id = fields.Many2one('budget.capex.cear',
                              string='Cear No')
    progress_id = fields.Many2one('budget.capex.progress',
                                  string='Progress')

    # CONSTRAINS
    # ----------------------------------------------------------
