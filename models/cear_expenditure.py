# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

from odoo.exceptions import UserError, ValidationError


class CearExpenditure(models.Model):
    _inherit = 'budget.capex.cear'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    # company_currency_id exist in cear_commitment
    is_expenditure = fields.Boolean(string='Is Expenditure')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    commitment_id = fields.Many2one('budget.capex.cear',
                                    string="Commitment Cear",
                                    domain=[('is_commitment', '=', True)]
                                    )

    # CONSTRAINS
    # ----------------------------------------------------------
    # expenditure_ids exist in cear model
    @api.one
    @api.constrains('is_expenditure')
    def _check_expenditure_ids(self):
        """
        Expenditure Can't have expenditure under
        """
        if self.is_expenditure and len(self.expenditure_ids) > 0:
            raise ValidationError("A Expenditure Cear Can't have it's own Expenditure Cear")

            # # total_expenditure_amount and total_commitment_amount
            # # exist in cear
            # @api.one
            # @api.constrains('total_expenditure_amount', 'total_commitment_amount', 'is_expenditure')
            # def _check_total_expenditure_total_commitment(self):
            #     """
            #     The Total Expenditure must not be greater than Total Commitment
            #     If not expenditure
            #     """
            #     if not self.is_expenditure and self.total_expenditure_amount > self.total_commitment_amount:
            #         raise ValidationError("Commitment Cear Total Expenditure Can't exceed Total Commitment")
