# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class ProgressLine(models.Model):
    _name = 'budget.capex.progress.line'
    _rec_name = 'name'
    _description = 'Cear Progress Line'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    asset_major = fields.Char(string='Asset Major')
    asset_minor = fields.Char(string='Asset Minor')
    asset_code = fields.Char(string='Asset Code')
    asset_description = fields.Text(string='Asset Description')
    rfs_date = fields.Date(string="RFS Date")
    name = fields.Char(string='Name')
    amount = fields.Monetary(string='Amount',
                             currency_field='currency_id',
                             store=True)
    remarks = fields.Text(string="Remarks")

    # RELATED FIELDS
    # ----------------------------------------------------------
    cear_description = fields.Text(related='cear_id.description',
                                   string='Cear Description',
                                   store=True)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    cear_id = fields.Many2one('budget.capex.cear',
                              string='Cear No')
    progress_id = fields.Many2one('budget.capex.progress',
                                  ondelete='cascade',
                                  string='Progress')
    cost_center_id = fields.Many2one('budget.core.cost.center', string='Cost Center')

    # CONSTRAINS
    # ----------------------------------------------------------
