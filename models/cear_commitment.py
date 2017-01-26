# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class Cear(models.Model):
    _name = 'budget.capex.cear'
    _rec_name = 'no'
    _description = 'Cear'
    _inherit = ['mail.thread']

    # CHOICES
    # ----------------------------------------------------------
    year_now = fields.Datetime.from_string(fields.Date.today()).year
    YEARS = [(year, year) for year in range(year_now - 10, year_now + 10)]
    STATES = choices_tuple(['draft', 'under process', 'authorized', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_commitment = fields.Boolean('Is Commitment')
    state = fields.Selection(STATES, default='draft')
    category = fields.Char(string="Category")
    year = fields.Selection(string='Year', selection=YEARS, default=year_now)

    no = fields.Char(string="Cear No", required=True)
    description = fields.Text(string="Cear Description")
    start_date = fields.Date(string="Cear Start Date")

    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                         string='Expenditure Amount')
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    pec_no = fields.Char(string="Pec No")
    remarks = fields.Text(string="Remarks")

    # ACTUAL FROM FINANCE
    fn_utilized_amount = fields.Monetary(currency_field='company_currency_id',
                                             string='Utilized Amount (FN)')
    # ACTUAL FROM FINANCE
    authorized_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Authorized Amount')
    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    expenditure_ids = fields.One2many('budget.capex.cear',
                                      'commitment_id',
                                      domain=[('is_expenditure', '=', True)],
                                      string="Expenditure Cears")

    progress_allocation_ids = fields.One2many('budget.capex.progress.allocation',
                                              'cear_id',
                                              string="Allocations")

    investment_area_id = fields.Many2one('budget.capex.cear.investment.area', string="Investment Area")
    region_id = fields.Many2one('budget.enduser.region', string="Region")
    project_id = fields.Many2one('budget.core.budget',
                                 domain=[('is_project', '=', True),
                                         ('state', 'not in', ['draft'])],
                                 string='Project No'
                                 )

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
        ('uniq_no', 'UNIQUE (no)', 'Cear No Must Be unique')
    ]
