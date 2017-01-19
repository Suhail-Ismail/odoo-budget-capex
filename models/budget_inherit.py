# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class BudgetInherit(models.Model):
    _inherit = 'budget.core.budget'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    task_ids = fields.One2many('budget.capex.task',
                               'project_id',
                               string="Projects")

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    overall_progress = fields.Float(compute='_compute_overall_progress',
                                    string='Overall Progress',
                                    store=True)

    total_task_expenditure_amount = fields.Monetary(compute='_compute_total_task_expenditure_amount',
                                                    currency_field='company_currency_id',
                                                    string='Total Task Expenditure Amount',
                                                    store=True)

    total_task_commitment_amount = fields.Monetary(compute='_compute_total_task_commitment_amount',
                                                   currency_field='company_currency_id',
                                                   string='Total Task Commitment Amount',
                                                   store=True)

    balance_expenditure_amount = fields.Monetary(compute='_compute_balance_expenditure_amount',
                                                 currency_field='company_currency_id',
                                                 string='Balance Commitment Amount',
                                                 store=True)

    balance_commitment_amount = fields.Monetary(compute='_compute_balance_commitment_amount',
                                                currency_field='company_currency_id',
                                                string='Balance Commitment Amount',
                                                store=True)

    @api.one
    @api.depends('task_ids', 'task_ids.progress', 'task_ids.state')
    def _compute_overall_progress(self):
        progress_list = self.task_ids.mapped('progress')
        if len(progress_list) > 0:
            self.overall_progress = sum(progress_list) / float(len(progress_list))
        else:
            self.overall_progress = 0

    @api.one
    @api.depends('task_ids', 'task_ids.expenditure_amount', 'task_ids.state')
    def _compute_total_task_expenditure_amount(self):
        self.total_task_expenditure_amount = sum(self.task_ids. \
                                           filtered(lambda r: r.state not in ['draft']). \
                                           mapped('expenditure_amount'))

    @api.one
    @api.depends('task_ids', 'task_ids.commitment_amount', 'task_ids.state')
    def _compute_total_task_commitment_amount(self):
        self.total_task_commitment_amount = sum(self.task_ids. \
                                                filtered(lambda r: r.state not in ['draft']). \
                                                mapped('commitment_amount'))

    @api.one
    @api.depends('commitment_amount', 'total_task_commitment_amount')
    def _compute_balance_commitment_amount(self):
        self.balance_commitment_amount = self.commitment_amount - self.total_task_commitment_amount

    @api.one
    @api.depends('expenditure_amount', 'total_task_expenditure_amount')
    def _compute_balance_expenditure_amount(self):
        self.balance_expenditure_amount = self.expenditure_amount - self.total_task_expenditure_amount

