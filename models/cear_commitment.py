# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Cear(models.Model):
    _name = 'budget.capex.cear'
    _rec_name = 'no'
    _description = 'Cear'
    _inherit = ['mail.thread', 'budget.enduser.mixin']

    # CHOICES
    # ----------------------------------------------------------
    year_now = fields.Datetime.from_string(fields.Date.today()).year
    YEARS = [(year, year) for year in range(1950, 2050)]
    STATES = choices_tuple(['draft', 'under process', 'authorized', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    # division_id, section_id, sub_section_id exist in enduser.mixin
    is_commitment = fields.Boolean('Is Commitment')
    is_recharge = fields.Boolean('Is Recharge')
    is_unforseen = fields.Boolean('Is Unforseen')
    is_non_engineering = fields.Boolean('Is Non Engineering')

    state = fields.Selection(STATES, default='draft')
    category = fields.Char(string="Category")
    year = fields.Selection(string='Year', selection=YEARS, default=year_now)

    no = fields.Char(string="Cear No", required=True)
    description = fields.Text(string="Cear Description")
    pec_no = fields.Char(string="Pec No")
    remarks = fields.Text(string="Remarks")
    system_note = fields.Text(string="System Note")

    completion_date = fields.Date(string="Completion Date")
    rfs_date = fields.Date(string="RFS Date")
    start_date = fields.Date(string="Cear Start Date")
    pec_no_date = fields.Date(string="Pec No Date")

    expenditure_amount = fields.Monetary(currency_field='currency_id',
                                         string='Expenditure Amount')
    commitment_amount = fields.Monetary(currency_field='currency_id',
                                        string='Commitment Amount')

    # ACTUAL FROM FINANCE
    fn_utilized_amount = fields.Monetary(currency_field='currency_id',
                                         string='Utilized Amount (FN)')
    # ACTUAL FROM FINANCE
    authorized_amount = fields.Monetary(currency_field='currency_id',
                                        string='Authorized Amount')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    expenditure_ids = fields.One2many('budget.capex.cear',
                                      'commitment_id',
                                      domain=[('is_expenditure', '=', True)],
                                      string="Expenditure Cears")
    accrual_line_ids = fields.One2many('budget.capex.accrual.line',
                                       'cear_id',
                                       string="Accruals")
    progress_line_ids = fields.One2many('budget.capex.progress.line',
                                        'cear_id',
                                        string="Progress Lines")
    contract_ids = fields.Many2many('budget.contractor.contract',
                                    'budget_cear_cear_contract',
                                    'cear_id',
                                    'contract_id',
                                    string='Contracts')
    contractor_ids = fields.Many2many('budget.contractor.contractor',
                                      'budget_cear_cear_contractor',
                                      'cear_id',
                                      'contractor_id',
                                      string='Contractors')

    investment_area_id = fields.Many2one('budget.capex.cear.investment.area', string="Investment Area")
    region_id = fields.Many2one('budget.enduser.region', string="Region")
    project_id = fields.Many2one('budget.core.budget',
                                 domain=[('is_project', '=', True),
                                         ('state', 'not in', ['draft'])],
                                 string='Project No'
                                 )

    # ONCHANGE FIELDS
    # ----------------------------------------------------------
    @api.onchange('contract_ids')
    def _onchange_contract_id(self):
        self.contractor_ids |= self.mapped('contract_ids.contractor_id')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_pcc_amount = fields.Monetary(string='Total PCC Amount',
                                       currency_field='currency_id',
                                       compute='_compute_total_pcc_amount',
                                       store=True)

    total_accrual_amount = fields.Monetary(string='Total Accrual Amount',
                                           currency_field='currency_id',
                                           compute='_compute_total_accrual_amount',
                                           store=True)

    # COMPUTE FUNCTION
    # ----------------------------------------------------------
    @api.one
    @api.depends('progress_line_ids', 'progress_line_ids.amount')
    def _compute_total_pcc_amount(self):
        self.total_pcc_amount = sum(self.mapped('progress_line_ids.amount'))

    @api.one
    @api.depends('accrual_line_ids', 'accrual_line_ids.amount')
    def _compute_total_accrual_amount(self):
        self.total_accrual_amount = sum(self.mapped('progress_line_ids.amount'))

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
        ('uniq_no', 'UNIQUE (no)', 'Cear No Must Be unique'),
        # TODO NEED TO CLEAN DATA TO APPLY THIS
        # ('pcc_less_or_eq_to_commitment', 'CHECK (total_pcc_amount <= commitment_amount)',
        # 'PCC must be less than or equal to commitment'),
        ('pcc_less_or_eq_to_commitment', 'CHECK (1 == 1)',
         'Temporary Disabled'),
    ]
