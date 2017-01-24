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
