# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class Task(models.Model):
    _name = 'budget.capex.task'
    _rec_name = 'task_no'
    _description = 'Task'
    _inherit = ['mail.thread']

    # CHOICES
    # ----------------------------------------------------------
    year_now = fields.Datetime.from_string(fields.Date.today()).year
    YEARS = [(year, year) for year in range(year_now - 10, year_now + 10)]
    STATES = choices_tuple(['draft', 'under process', 'authorized', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    category = fields.Char(string="Category")
    year = fields.Selection(string='Year', selection=YEARS, default=year_now)

    task_no = fields.Char(string="Task No", required=True)
    task_description = fields.Text(string="Task Description")
    task_start_date = fields.Date(string="Task Start Date")
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                         string='Expenditure Amount')
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    initial_progress = fields.Float(string='Initial Progress')
    pec_no = fields.Char(string="Pec No")
    remarks = fields.Text(string="Remarks")

    # TODO ACTUAL
    total_amount = fields.Monetary(currency_field='company_currency_id',
                                   string='Utilized Amount (FN)')
    # TODO ACTUAL
    authorized_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Authorized Amount (FN)')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    child_ids = fields.One2many('budget.capex.task',
                                'parent_id',
                                domain=[('is_child', '=', True)],
                                string="Parent Task")

    progress_ids = fields.One2many('budget.capex.task.progress',
                                   'task_id',
                                   string="Progress")

    task_investment_area_id = fields.Many2one('budget.capex.task.investment.area', string="Investment Area")
    region_id = fields.Many2one('budget.enduser.region', string="Region")
    project_id = fields.Many2one('budget.core.budget',
                                 domain=[('is_project', '=', True),
                                         ('state', 'not in', ['draft'])],
                                 string='Project'
                                 )

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_expenditure_amount = fields.Monetary(compute='_compute_total_expenditure_amount',
                                               currency_field='company_currency_id',
                                               string='Total Expenditure Amount',
                                               store=True)
    total_commitment_amount = fields.Monetary(compute='_compute_total_commitment_amount',
                                              currency_field='company_currency_id',
                                              string='Total Commitment Amount',
                                              store=True)
    accrual_amount = fields.Monetary(compute='_compute_accrual_amount',
                                     currency_field='company_currency_id',
                                     string='Accrual Amount',
                                     store=True)
    progress = fields.Float(compute='_compute_progress',
                            string='Progress',
                            store=True)

    @api.one
    @api.depends('child_ids', 'child_ids.expenditure_amount', 'child_ids.state', 'state')
    def _compute_total_expenditure_amount(self):
        self.total_expenditure_amount = sum(self.child_ids. \
                                            filtered(lambda r: r.state not in ['draft']). \
                                            mapped('expenditure_amount'))
        if self.state not in ['draft']:
            self.total_expenditure_amount += self.expenditure_amount

    @api.one
    @api.depends('child_ids', 'child_ids.commitment_amount', 'child_ids.state', 'state')
    def _compute_total_commitment_amount(self):
        self.total_commitment_amount = sum(self.child_ids. \
                                            filtered(lambda r: r.state not in ['draft']). \
                                            mapped('commitment_amount'))
        if self.state not in ['draft']:
            self.total_commitment_amount += self.commitment_amount

    @api.one
    @api.depends('progress_ids', 'progress_ids.accrual_amount')
    def _compute_accrual_amount(self):
        self.accrual_amount = sum(self.progress_ids.mapped('accrual_amount'))

    @api.one
    @api.depends('progress_ids', 'progress_ids.progress')
    def _compute_progress(self):
        self.progress = sum(self.progress_ids.mapped('progress'))

    # TRANSITIONS
    # ----------------------------------------------------------
    def set2draft(self):
        self.state = 'draft'

    def set2under_process(self):
        self.state = 'under process'

    def set2authorize(self):
        self.state = 'authorized'

    def set2close(self):
        self.state = 'closed'

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_task_no', 'UNIQUE (task_no)', 'Task No Must Be unique')
    ]

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not values.get('progress_ids', False):
            initial_progress = values.get('initial_progress', 0.00)
            name = values.get('name', '')
            start_date = values.get('start_date', False)

            progress = {
                'name': 'INITIAL: %s' % name,
                'remarks': 'initial progress',
                'progress': initial_progress,
                'change_date': start_date,
                'is_initial': True
            }

            values.update(progress_ids=[(0, 0, progress)])

        return super(Task, self).create(values)
