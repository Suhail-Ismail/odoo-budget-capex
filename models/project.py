# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .utils import choices_tuple

class Project(models.Model):
    _name = 'budget.project'
    _rec_name = 'project_no'
    _description = 'Project'

    # BASIC FIELDS
    # ----------------------------------------------------------
    project_no = fields.Char(string="Project No", required=True)
    project_date = fields.Date(string="Project Date")
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Expenditure Amount')
    description = fields.Text(string="Description")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    section_id = fields.Many2one('res.partner', string='Section',
                                 domain=[('is_budget_section','=',True)])
    sub_section_id = fields.Many2one('res.partner', string='Sub Section',
                                 domain=[('is_budget_sub_section','=',True)])
    task_ids = fields.One2many('budget.task',
                               'project_id',
                               string="Tasks")