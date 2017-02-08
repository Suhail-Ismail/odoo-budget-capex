# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Progress(models.Model):
    _name = 'budget.capex.progress'
    _rec_name = 'name'
    _description = 'Cear Progress'
    _order = 'progress_date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string='Name')
    is_initial = fields.Boolean(string='Is Initial')
    progress_date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    progress_allocation_ids = fields.One2many('budget.capex.progress.allocation',
                                              'progress_id',
                                              string="Allocations")

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    progress_amount = fields.Monetary(string='Progress Amount',
                                      compute='_compute_progress_amount',
                                      currency_field='company_currency_id',
                                      store=True)

    @api.one
    @api.depends('progress_allocation_ids')
    def _compute_progress_amount(self):
        self.progress_amount = sum(self.progress_allocation_ids.mapped('allocated_amount'))