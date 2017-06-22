# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Progress(models.Model):
    _name = 'budget.capex.progress'
    _rec_name = 'reference_no'
    _description = 'Cear Progress'
    _order = 'progress_date'
    _inherit = ['budget.enduser.mixin']

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    # division_id, section_id, sub_section_id exist in enduser.mixin
    reference_no = fields.Char(string='Reference No')
    is_initial = fields.Boolean(string='Is Initial')
    progress_date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------
    cwp_description = fields.Text(related='project_id.description',
                                  string='CWP Description',
                                  store=True)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    progress_line_ids = fields.One2many('budget.capex.progress.line',
                                        'progress_id',
                                        string="Progress Lines")
    project_id = fields.Many2one('budget.core.budget', string='CWP', domain=[('is_project', '=', True)])

    # ONCHANGE FIELDS
    # ----------------------------------------------------------
    @api.multi
    @api.onchange('project_id')
    def onchange_budget_line_ids(self):
        # division_id, section_id exist in enduser.mixin
        self.division_id = self.project_id.division_id
        self.section_id = self.project_id.section_id

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    progress_amount = fields.Monetary(string='Progress Amount',
                                      compute='_compute_progress_amount',
                                      currency_field='company_currency_id',
                                      store=True)

    @api.one
    @api.depends('progress_line_ids')
    def _compute_progress_amount(self):
        self.progress_amount = sum(self.progress_line_ids.mapped('amount'))

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_reference_no', 'UNIQUE (reference_no)', 'Reference No Exist'),
    ]
