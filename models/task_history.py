# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_core.models.utilities import choices_tuple


class TaskHistory(models.Model):
    _name = 'budget.capex.task.history'
    _rec_name = 'name'
    _description = 'Task History'
    _order = 'change_date'

    # CHOICES
    # ----------------------------------------------------------
    OPTIONS = choices_tuple(['add', 'subtract'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string='Name')
    is_initial = fields.Boolean(string='Is Initial')

    action_taken = fields.Selection(string='Action Taken', selection=OPTIONS, default='add')
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                         string='Expenditure Amount')
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    change_date = fields.Date(string="Change Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    task_id = fields.Many2one('budget.capex.task',
                              string="Task No")

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('expenditure_must_not_be_negative', 'CHECK (expenditure_amount >= 0)', 'Expenditure Amount Must Be Positive'),
        ('commitment_must_not_be_negative', 'CHECK (commitment_amount >= 0)', 'COmmitment Amount Must Be Positive'),

    ]
