# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Progress(models.Model):
    _name = 'budget.capex.progress'
    _rec_name = 'reference_no'
    _description = 'Cear Progress'
    _order = 'received_date'
    _inherit = ['budget.enduser.mixin']

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    # division_id, section_id, sub_section_id exist in enduser.mixin
    reference_no = fields.Char(string='Reference No', default='(Reference is Auto Generated)')
    received_date = fields.Date(string="Received Date")
    signed_date = fields.Date(string="Signed Date")
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    currency_id = fields.Many2one('res.currency', readonly=True,
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
                                      currency_field='currency_id',
                                      store=True)

    @api.one
    @api.depends('progress_line_ids')
    def _compute_progress_amount(self):
        self.progress_amount = sum(self.progress_line_ids.mapped('amount'))

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_reference_no', 'UNIQUE (reference_no)', 'Reference No Must Be Unique'),
    ]

    # MISC FUNCTIONS
    # ----------------------------------------------------------
    @api.model
    def _generate_reference_no(self, vals):
        received_date = fields.Date.from_string(vals['received_date'])
        year = received_date if not received_date else received_date.year
        section_id = self.env['budget.enduser.section'].browse(vals['section_id'])
        sr = 1

        if year and section_id:
            sql = """
                SELECT * FROM (
                  SELECT section_id, reference_no, date_part('year', received_date) AS year
                  FROM budget_capex_progress
                  ORDER BY id DESC) n
                WHERE n.year=%(year)d
                AND n.section_id=%(section_id)d
            """ % {
                'year': year,
                'section_id': section_id.id
            }
            self.env.cr.execute(sql)
            result = self.env.cr.dictfetchone()
            if result:
                sr = result['reference_no'].split('-')[-1]
                sr = int(sr) + 1

        return '{}-{}-{:03d}'.format(section_id.alias, year, sr)

    # POLYMORPH FUNCTIONS
    # ----------------------------------------------------------
    @api.model
    def create(self, vals):
        vals['reference_no'] = self._generate_reference_no(vals)
        return super(Progress, self).create(vals)
