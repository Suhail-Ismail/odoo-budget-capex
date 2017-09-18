# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class AccrualLine(models.Model):
    _name = 'budget.capex.accrual.line'
    _description = 'Cear Accrual Line'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    physical_progress = fields.Monetary(string='Pysical Progress (%)',
                                        currency_field='currency_id',
                                        help='Progress in terms of work completion in percentage (ie. 60% progress)',
                                        store=True)
    milestone = fields.Char(string='Milestone',
                            help="Milestone completed against progress % (ie. Delivery + Partial service, RFS, PAC, "
                                 "etc)")
    amount = fields.Monetary(string='Work Done Value',
                             currency_field='currency_id',
                             help="Value of Equipment or Services physically received in store or at site.",
                             store=True)
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    accrual_id = fields.Many2one('budget.capex.accrual',
                                 string='Accrual')
    cear_id = fields.Many2one('budget.capex.cear',
                              string='Cear No')
    currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    # CONSTRAINS
    # ----------------------------------------------------------
