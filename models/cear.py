# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple

from odoo.exceptions import ValidationError


class Cear(models.Model):
    _name = 'budget.capex.cear'
    _rec_name = 'unique_identifier'
    _description = 'Cear'
    _inherit = ['mail.thread', 'budget.enduser.mixin']

    # TODO DEPRECATE
    # ----------------------------------------------------------
    is_recharge = fields.Boolean('Is Recharge')
    is_unforseen = fields.Boolean('Is Unforseen')
    is_non_engineering = fields.Boolean('Is Non Engineering')
    is_commitment = fields.Boolean('Is Commitment')
    is_expenditure = fields.Boolean('Is Expenditure')
    # ----------------------------------------------------------

    # CHOICES
    # ----------------------------------------------------------
    year_now = fields.Datetime.from_string(fields.Date.today()).year
    YEARS = [(year, year) for year in range(1950, 2050)]
    STATES = choices_tuple(['draft', 'under process', 'authorized', 'closed'], is_sorted=False)
    TYPES = choices_tuple(['main', 'related', 'distributed', 'virtual'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    # division_id, section_id, sub_section_id exist in enduser.mixin
    has_distribution = fields.Boolean(default=False)

    state = fields.Selection(STATES, default='authorized')
    category = fields.Char(string='Category')
    year = fields.Selection(string='Year', selection=YEARS, default=year_now)

    input_no = fields.Char(string='Cear No')
    description = fields.Text(string='Cear Description')
    pec_no = fields.Char(string='Pec No')
    remarks = fields.Text(string='Remarks')
    system_note = fields.Text(string='System Note')

    completion_date = fields.Date(string='Completion Date')
    rfs_date = fields.Date(string='RFS Date')
    start_date = fields.Date(string='Cear Start Date')
    pec_no_date = fields.Date(string='Pec No Date')

    input_expenditure_amount = fields.Monetary(string='Expenditure Amount',
                                               currency_field='currency_id')
    input_commitment_amount = fields.Monetary(string='Commitment Amount',
                                              currency_field='currency_id')
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
    parent_id = fields.Many2one('budget.capex.cear',
                                domain='[("real_cear_id", "=", False), ("has_distribution", "=", False)]',
                                string='Parent Cear')
    child_ids = fields.One2many('budget.capex.cear',
                                'parent_id',
                                string='Child Cears')

    # THIS IS FOR MAKING BULK CEAR A.K.A. CREATING 1 CEAR WITH MULTIPLE LINE TO DISTRIBUTE THE AMOUNT
    real_cear_id = fields.Many2one('budget.capex.cear',
                                   ondelete='cascade',
                                   string='Real Cear')
    distribution_ids = fields.One2many('budget.capex.cear',
                                       'real_cear_id',
                                       string='Distributed Cears')

    member_ids = fields.One2many('budget.capex.cear',
                                 'group_id',
                                 string='Member Cears')

    accrual_line_ids = fields.One2many('budget.capex.accrual.line',
                                       'cear_id',
                                       string='Accruals')
    progress_line_ids = fields.One2many('budget.capex.progress.line',
                                        'cear_id',
                                        string='Progress Lines')
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
    investment_area_id = fields.Many2one('budget.capex.cear.investment.area', string='Investment Area')
    region_id = fields.Many2one('budget.enduser.region', string='Region')
    project_id = fields.Many2one('budget.core.budget',
                                 domain=[('is_project', '=', True),
                                         ('state', 'not in', ['draft'])],
                                 string='Project No')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    no = fields.Char(string='Computed Cear No',
                     compute='_compute_no',
                     store=True)

    # THIS IS FOR MAKING BULK CEAR A.K.A. CREATING 1 CEAR WITH MULTIPLE LINE TO DISTRIBUTE THE AMOUNT
    unique_identifier = fields.Char(string='Unique Identifier',
                                    compute='_compute_unique_identifier',
                                    store=True)
    type = fields.Selection(string='Type',
                            selection=TYPES,
                            compute='_compute_type',
                            store=True)
    group_id = fields.Many2one('budget.capex.cear', string='Group',
                               compute='_compute_group_id',
                               store=True)
    expenditure_amount = fields.Monetary(string='Computed Expenditure',
                                         currency_field='currency_id',
                                         compute='_compute_expenditure_amount',
                                         store=True)
    commitment_amount = fields.Monetary(string='Computed Commitment',
                                        currency_field='currency_id',
                                        compute='_compute_commitment_amount',
                                        store=True)
    total_commitment_amount = fields.Monetary(string='Total Commitment',
                                              currency_field='currency_id',
                                              compute='_compute_total_commitment_amount',
                                              store=True)
    total_expenditure_amount = fields.Monetary(string='Total Expenditure',
                                               currency_field='currency_id',
                                               compute='_compute_total_expenditure_amount',
                                               store=True)
    total_pcc_amount = fields.Monetary(string='Total PCC Amount',
                                       currency_field='currency_id',
                                       compute='_compute_total_pcc_amount',
                                       store=True)
    total_accrual_amount = fields.Monetary(string='Total Accrual Amount',
                                           currency_field='currency_id',
                                           compute='_compute_total_accrual_amount',
                                           store=True)
    percent_pcc = fields.Float(string='Progress',
                               digits=(5, 2),
                               compute='_compute_percent_pcc',
                               store=True)

    percent_accrual = fields.Float(string='Accrual',
                                   digits=(5, 2),
                                   compute='_compute_percent_accrual',
                                   store=True)

    @api.one
    @api.depends('input_no', 'real_cear_id', 'real_cear_id.input_no')
    def _compute_no(self):
        if self.real_cear_id and self.real_cear_id.input_no:
            self.no = self.real_cear_id.input_no
        elif self.input_no:
            self.no = self.input_no
        return

    @api.one
    @api.depends('type', 'no', 'real_cear_id.no')
    def _compute_unique_identifier(self):
        if self.type == 'related':
            self.unique_identifier = 'Related:%s' % self.no
        elif self.type == 'virtual':
            self.unique_identifier = 'Virtual:%s:%s' % (self.real_cear_id.no, self.parent_id.no)
        elif self.type == 'distributed':
            self.unique_identifier = 'Distributed:%s' % self.no
        elif self.type == 'main':
            self.unique_identifier = 'Main:%s' % self.no
        else:
            self.unique_identifier = False

    @api.one
    @api.depends('has_distribution', 'real_cear_id', 'parent_id')
    def _compute_type(self):
        if self.has_distribution:
            self.type = 'distributed'
        elif not self.real_cear_id and self.parent_id:
            self.type = 'related'
        elif self.real_cear_id and self.parent_id:
            self.type = 'virtual'
        else:
            self.type = 'main'

    @api.one
    @api.depends('parent_id')
    def _compute_group_id(self):
        if self.parent_id:
            mapped_string = 'parent_id'
            while True:
                cear_ids = self.mapped(mapped_string)
                if not cear_ids:
                    break
                self.group_id = self.mapped(mapped_string)
                mapped_string += '.parent_id'
            return

        self.group_id = self
        return

    @api.one
    @api.depends('input_commitment_amount', 'type', 'distribution_ids', 'distribution_ids.commitment_amount')
    def _compute_commitment_amount(self):
        if self.type == 'distributed':
            self.commitment_amount = sum(self.distribution_ids.mapped('input_commitment_amount'))
        else:
            self.commitment_amount = self.input_commitment_amount

    @api.one
    @api.depends('input_expenditure_amount', 'type', 'distribution_ids', 'distribution_ids.expenditure_amount')
    def _compute_expenditure_amount(self):
        if self.type == 'distributed':
            self.expenditure_amount = sum(self.distribution_ids.mapped('input_expenditure_amount'))
        else:
            self.expenditure_amount = self.input_expenditure_amount

    @api.one
    @api.depends('commitment_amount', 'child_ids',
                 'child_ids.total_commitment_amount', 'child_ids.commitment_amount')
    def _compute_total_commitment_amount(self):
        ids = self.get_related_cear_ids()
        cear_ids = self.browse(ids)
        self.total_commitment_amount = sum(cear_ids.mapped('commitment_amount'))

    @api.one
    @api.depends('expenditure_amount', 'child_ids',
                 'child_ids.total_expenditure_amount', 'child_ids.expenditure_amount')
    def _compute_total_expenditure_amount(self):
        ids = self.get_related_cear_ids()
        cear_ids = self.browse(ids)
        self.total_expenditure_amount = sum(cear_ids.mapped('expenditure_amount'))

    @api.one
    @api.depends('progress_line_ids', 'progress_line_ids.amount', 'child_ids.total_pcc_amount')
    def _compute_total_pcc_amount(self):
        ids = self.get_related_cear_ids()
        cear_ids = self.browse(ids)
        self.total_pcc_amount = sum(cear_ids.mapped('progress_line_ids.amount'))

    @api.one
    @api.depends('accrual_line_ids', 'accrual_line_ids.amount', 'child_ids.total_accrual_amount')
    def _compute_total_accrual_amount(self):
        ids = self.get_related_cear_ids()
        cear_ids = self.browse(ids)
        self.total_accrual_amount = sum(cear_ids.mapped('accrual_line_ids.amount'))

    @api.one
    @api.depends('total_pcc_amount', 'total_expenditure_amount')
    def _compute_percent_pcc(self):
        if self.total_expenditure_amount:
            percent = self.total_pcc_amount / self.total_expenditure_amount
        else:
            percent = 0
        self.percent_pcc = percent * 100

    @api.one
    @api.depends('total_accrual_amount', 'total_expenditure_amount')
    def _compute_percent_accrual(self):
        if self.total_expenditure_amount:
            percent = self.total_accrual_amount / self.total_expenditure_amount
        else:
            percent = 0
        self.percent_accrual = percent * 100

    # INVERSE FIELDS
    # ----------------------------------------------------------

    # ONCHANGE FIELDS
    # ----------------------------------------------------------
    @api.onchange('contract_ids')
    def _onchange_contract_id(self):
        self.contractor_ids |= self.mapped('contract_ids.contractor_id')

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_no', 'UNIQUE (unique_identifier)',
         'Cear No or CEAR Distribution Must Be unique'),
        # (
        #     'exp_less_or_eq_commitment',
        #     'CHECK (parent_id IS NOT NULL OR total_expenditure_amount <= total_commitment_amount)',
        #     'Expenditure <= Commitment'
        # ),
        (
            'parent_id_no_equal_child_id',
            'CHECK (id != parent_id)',
            'Temporary Disabled'
        ),
        (
            'pcc_less_or_eq_to_commitment',
            'CHECK (1=1)',
            'Temporary Disabled'
        ),
        (
            'exp_less_or_eq_commitment',
            'CHECK (1=1)',
            'Temporary Disabled'
        ),

    ]

    # TODO CHECK THIS VALIDATION
    # @api.one
    # @api.constrains('has_distribution', 'distribution_ids', 'parent_id')
    # def _check_distribution_ids_must_be_parent(self):
    #     if not self.parent_id and (self.has_distribution or self.distribution_ids):
    #         return
    #     raise ValidationError('Distributed CEAR must be a parent CEAR')

    # @api.one
    # @api.constrains('has_distribution', 'distribution_ids')
    # def _check_has_distribution_must_have_distribution(self):
    #     if self.has_distribution and len(self.distribution_ids) == 0:
    #         raise ValidationError('Distributed CEAR must have distribution CEAR in financial tab')
    #     return

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

    # ACTION BUTTONS
    # ----------------------------------------------------------
    def show_child_accruals(self):
        tree_id = self.env.ref('budget_capex.view_tree_accrual_line').id
        res = {
            'name': 'Child Accruals',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'budget.capex.accrual.line',
            'domain': [("cear_id", "=", self.id)],
            'views': [(tree_id, 'tree')],
        }
        return res

    def show_related_accruals(self):
        ids = self.get_related_cear_ids()
        res = self.show_child_accruals()
        res['name'] = 'Related Accruals'
        res['domain'] = [("cear_id", "in", ids)]
        return res

    def show_child_pccs(self):
        tree_id = self.env.ref('budget_capex.view_tree_progress_line').id
        res = {
            'name': 'Child PCCs',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'budget.capex.progress.line',
            'domain': [("cear_id", "=", self.id)],
            'views': [(tree_id, 'tree')],
        }
        return res

    def show_related_pccs(self):
        ids = self.get_related_cear_ids()
        res = self.show_child_pccs()
        res['name'] = 'Related PCCs'
        res['domain'] = [("cear_id", "in", ids)]
        return res

    def show_child_cears(self):
        tree_id = self.env.ref('budget_capex.view_tree_cear').id
        form_id = self.env.ref('budget_capex.view_form_cear').id
        search_id = self.env.ref('budget_capex.search_cear').id
        res = {
            'name': 'Child CEARs',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'budget.capex.cear',
            'domain': [("parent_id", "=", self.id)],
            'views': [(tree_id, 'tree'), (form_id, 'form'), (search_id, 'search')],
        }
        return res

    def show_related_cears(self):
        ids = self.get_related_cear_ids()
        res = self.show_child_cears()
        res['name'] = 'Related CEARs'
        res['domain'] = [("id", "in", ids)]
        return res

    # MISC FUNCTIONS
    # ----------------------------------------------------------
    @api.model
    def get_related_cear_ids(self):
        """
        get the ids related to the given cear including its own id
        """
        ids = [self.id]
        mapped_string = 'child_ids'

        while True:
            temp_ids = self.mapped(mapped_string).ids
            if not temp_ids:
                break

            ids += temp_ids
            mapped_string += '.child_ids'

        return ids

    # POLYMORPH FUNCTIONS
    # ----------------------------------------------------------