# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .utils import choices_tuple


class Project(models.Model):
    _name = 'budget.project'
    _rec_name = 'project_no'
    _description = 'Project'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'active', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    project_no = fields.Char(string="Project No", required=True)
    project_date = fields.Date(string="Project Date")
    description = fields.Text(string="Description")

    # Initial Amounts are use to create the first history
    initial_commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                                string='Commitment Amount',
                                                required=True)
    initial_expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                                 string='Expenditure Amount',
                                                 required=True)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    commitment_amount = fields.Monetary(compute='_compute_commitment_amount',
                                        currency_field='company_currency_id',
                                        string='Commitment Amount',
                                        store=True)
    expenditure_amount = fields.Monetary(compute='_compute_expenditure_amount',
                                         currency_field='company_currency_id',
                                         string='Expenditure Amount',
                                         store=True)

    @api.one
    @api.depends('project_history_ids', 'project_history_ids.commitment_amount')
    def _compute_commitment_amount(self):
        self.commitment_amount = sum(self.project_history_ids.mapped('commitment_amount'))

    @api.one
    @api.depends('project_history_ids', 'project_history_ids.expenditure_amount')
    def _compute_expenditure_amount(self):
        self.expenditure_amount = sum(self.project_history_ids.mapped('expenditure_amount'))

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    section_id = fields.Many2one('res.partner', string='Section',
                                 domain=[('is_budget_section', '=', True)])
    sub_section_id = fields.Many2one('res.partner', string='Sub Section',
                                     domain=[('is_budget_sub_section', '=', True)])
    project_history_ids = fields.One2many('budget.project.history',
                                          'project_id',
                                          string="Histories")
    task_ids = fields.One2many('budget.task',
                               'project_id',
                               string="Tasks")

    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        # Remove any History Created, as it will conflict with the logic
        values.update(project_history_ids=False)

        project = super(Project, self).create(values)
        self.env['budget.project.history'].create({
            'option': 'add',
            'commitment_amount': project.initial_commitment_amount,
            'expenditure_amount': project.initial_expenditure_amount,
            'change_date': project.project_date,
            'remarks': 'initial amount',
            'project_id': project.id,
            'from_project_id': project.id,
            'to_project_id': project.id
        })

        return project
