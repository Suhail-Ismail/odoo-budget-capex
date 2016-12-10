# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_core.models.utilities import choices_tuple


class TaskProgress(models.Model):
    _name = 'budget.capex.task.progress'
    _rec_name = 'name'
    _description = 'Task Progress'
    _order = 'change_date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string='Name')
    is_initial = fields.Boolean(string='Is Initial')

    progress = fields.Float(string='Progress (%)')
    change_date = fields.Date(string="Change Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    task_id = fields.Many2one('budget.capex.task',
                              ondelete='cascade',
                              string="Task")

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('progress', 'CHECK (progress >= 0 and progress < 100)', 'Progress must be between 0-100')
    ]

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    accrual_amount = fields.Monetary(compute='_compute_accrual_amount',
                                         currency_field='company_currency_id',
                                         string='Accrual Amount',
                                         store=True)

    @api.one
    @api.depends('progress')
    def _compute_accrual_amount(self):
        self.accrual_amount = self.task_id.commitment_amount * self.progress / 100