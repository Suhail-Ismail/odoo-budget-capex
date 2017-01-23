# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple


class BudgetInherit(models.Model):
    _inherit = 'budget.core.budget'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    cear_ids = fields.One2many('budget.capex.cear',
                               'project_id',
                               string="Projects")

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # total_cear_expenditure_amount = fields.Monetary(compute='_compute_total_cear_expenditure_amount',
    #                                                 currency_field='company_currency_id',
    #                                                 string='Total Cear Expenditure Amount',
    #                                                 store=True)
    #
    # total_cear_commitment_amount = fields.Monetary(compute='_compute_total_cear_commitment_amount',
    #                                                currency_field='company_currency_id',
    #                                                string='Total Cear Commitment Amount',
    #                                                store=True)
    #
    # balance_expenditure_amount = fields.Monetary(compute='_compute_balance_expenditure_amount',
    #                                              currency_field='company_currency_id',
    #                                              string='Balance Commitment Amount',
    #                                              store=True)
    #
    # balance_commitment_amount = fields.Monetary(compute='_compute_balance_commitment_amount',
    #                                             currency_field='company_currency_id',
    #                                             string='Balance Commitment Amount',
    #                                             store=True)
    #
    # @api.one
    # @api.depends('cear_ids', 'cear_ids.expenditure_amount', 'cear_ids.state')
    # def _compute_total_cear_expenditure_amount(self):
    #     self.total_cear_expenditure_amount = sum(self.cear_ids. \
    #                                        filtered(lambda r: r.state not in ['draft']). \
    #                                        mapped('expenditure_amount'))
    #
    # @api.one
    # @api.depends('cear_ids', 'cear_ids.commitment_amount', 'cear_ids.state')
    # def _compute_total_cear_commitment_amount(self):
    #     self.total_cear_commitment_amount = sum(self.cear_ids. \
    #                                             filtered(lambda r: r.state not in ['draft']). \
    #                                             mapped('commitment_amount'))
    #
    # @api.one
    # @api.depends('commitment_amount', 'total_cear_commitment_amount')
    # def _compute_balance_commitment_amount(self):
    #     self.balance_commitment_amount = self.commitment_amount - self.total_cear_commitment_amount
    #
    # @api.one
    # @api.depends('expenditure_amount', 'total_cear_expenditure_amount')
    # def _compute_balance_expenditure_amount(self):
    #     self.balance_expenditure_amount = self.expenditure_amount - self.total_cear_expenditure_amount
    #
