# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class Accrual(models.Model):
    _name = 'budget.capex.accrual'
    _rec_name = 'accrual_date'
    _description = 'Cear Accrual'
    _order = 'accrual_date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    accrual_date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    accrual_line_ids = fields.One2many('budget.capex.accrual.line',
                                       'accrual_id',
                                       string="Accrual Lines")

    # ONCHANGE FIELDS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------
