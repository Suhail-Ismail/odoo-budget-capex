# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Progress(models.Model):
    _name = 'budget.capex.progress'
    _rec_name = 'reference_no'
    _description = 'Cear Progress'
    _order = 'progress_date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
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
    # TODO TRASFERING SECTION TO DIVISION
    division_id = fields.Many2one('budget.enduser.section', string="Division")
    section_id = fields.Many2one('budget.enduser.section', string='Section')
    sub_section_id = fields.Many2one('budget.enduser.sub.section', string='Sub Section')

    # ONCHANGE FIELDS
    # ----------------------------------------------------------
    # TODO NEED TO FIX THIS FUNCTION TO REPLACE SECTION TO DIVISION
    @api.multi
    @api.onchange('project_id')
    def onchange_budget_line_ids(self):
        self.section_id = self.project_id.section_id
        self.sub_section_id = self.project_id.sub_section_id

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
