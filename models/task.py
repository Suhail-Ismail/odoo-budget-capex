# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .utils import choices_tuple

class Task(models.Model):
    _name = 'budget.task'
    _rec_name = 'task_no'
    _description = 'Task'

    # CHOICES
    # ----------------------------------------------------------
    year_now = fields.Datetime.from_string(fields.Date.today()).year
    YEARS = [(year, year) for year in range(year_now - 5, year_now + 5)]
    STATES = choices_tuple(['draft', 'active', 'closed'])

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

    authorized_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Authorized Amount')
    current_year = fields.Monetary(currency_field='company_currency_id',
                                   string='Current Year Amount')
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
    region_id = fields.Many2one('budget.region', string="Region")
    project_id = fields.Many2one('budget.project', string="Project")

    # COMPUTE FIELDS
    # TODO: This goes to invoice module via inheritance
    # ----------------------------------------------------------
    # invoice_ids
    # utilized_amount = fields.Monetary(currency_field='company_currency_id',
    #                                   string='Utilized Amount (IM)',
    #                                   compute='_compute_utilized_amount',
    #                                   store=True)

