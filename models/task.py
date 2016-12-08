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
    task_class = fields.Char(string="Task Class")
    task_description = fields.Text(string="Task Description")
    task_owner = fields.Char(string="Task Owner")
    task_created_by = fields.Char(string="Task Create By")
    task_start_date = fields.Date(string="Task Start Date")
    task_completion_date = fields.Date(string="Task Completion Date")
    task_status = fields.Char(string="Task Status")

    # TODO ACTUAL
    authorized_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Authorized Amount (FN)')
    initial_expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                                 string='Initial Expenditure Amount')
    initial_commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                                string='Initial Commitment Amount')
    initial_progress = fields.Float(string='Initial Progress')
    current_year = fields.Monetary(currency_field='company_currency_id',
                                   string='Current Year Amount')
    # TODO ACTUAL
    total_amount = fields.Monetary(currency_field='company_currency_id',
                                   string='Utilized Amount (FN)')

    transferable_amount = fields.Monetary(currency_field='company_currency_id',
                                          string='Transferable Amount')
    current_month_exp_amount = fields.Monetary(currency_field='company_currency_id',
                                               string='Current Month Expenditure Amount')
    completion = fields.Integer(string="Completion")

    last_pcc_date = fields.Date(string="Last PCC Date")
    expected_completion_date = fields.Date(string="Expected Completion Date")
    last_followed_date = fields.Date(string="Last Followed Date")
    major_type = fields.Char(string="Major Type")
    minor_sub_type = fields.Char(string="Minor Sub Type")
    gl_code = fields.Char(string="GL Code")
    pec_no = fields.Char(string="Pec No")

    notes = fields.Text(string="Notes")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    history_ids = fields.One2many('budget.capex.task.history',
                                  'task_id',
                                  string="Invoices")

    progress_ids = fields.One2many('budget.capex.task.progress',
                                   'task_id',
                                   string="Invoices")

    task_investment_area_id = fields.Many2one('budget.capex.task.investment.area', string="Investment Area")
    region_id = fields.Many2one('budget.enduser.region', string="Region")
    project_id = fields.Many2one('budget.core.budget',
                                 domain=[('is_project', '=', True),
                                         ('state', 'not in', ['draft'])],
                                 string="Project"
                                 )

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    expenditure_amount = fields.Monetary(compute='_compute_expenditure_amount',
                                         currency_field='company_currency_id',
                                         string='Expenditure Amount',
                                         store=True)
    commitment_amount = fields.Monetary(compute='_compute_commitment_amount',
                                        currency_field='company_currency_id',
                                        string='Commitment Amount',
                                        store=True)
    accrual_amount = fields.Monetary(compute='_compute_accrual_amount',
                                     currency_field='company_currency_id',
                                     string='Accrual Amount',
                                     store=True)
    progress = fields.Float(compute='_compute_progress',
                            string='Progress',
                            store=True)

    @api.one
    @api.depends('history_ids', 'history_ids.expenditure_amount')
    def _compute_expenditure_amount(self):
        for history in self.history_ids:
            if history.action_taken in ['add']:
                self.expenditure_amount += history.expenditure_amount
            elif history.action_taken in ['subtract']:
                self.expenditure_amount -= history.expenditure_amount

    @api.one
    @api.depends('history_ids', 'history_ids.commitment_amount')
    def _compute_commitment_amount(self):
        for history in self.history_ids:
            if history.action_taken in ['add']:
                self.commitment_amount += history.commitment_amount
            elif history.action_taken in ['subtract']:
                self.commitment_amount -= history.commitment_amount

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
        if not values.get('history_ids', False):
            initial_expenditure_amount = values.get('initial_expenditure_amount', 0.00)
            initial_commitment_amount = values.get('initial_commitment_amount', 0.00)
            initial_progress = values.get('initial_progress', 0.00)
            name = values.get('name', '')
            start_date = values.get('start_date', False)
            # create Initial history
            history = {
                'name': 'INITIAL: %s' % name,
                'remarks': 'initial amount',
                'expenditure_amount': initial_expenditure_amount,
                'commitment_amount': initial_commitment_amount,
                'action_taken': 'add',
                'change_date': start_date,
                'is_initial': True
            }
            progress = {
                'name': 'INITIAL: %s' % name,
                'remarks': 'initial progress',
                'progress': initial_progress,
                'change_date': start_date,
                'is_initial': True
            }

            values.update(history_ids=[(0, 0, history)])
            values.update(progress_ids=[(0, 0, progress)])

        return super(Task, self).create(values)
