# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

from odoo.exceptions import UserError, ValidationError


class TaskExpenditure(models.Model):
    _inherit = 'budget.capex.task'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    commitment_id = fields.Many2one('budget.capex.task',
                                string="Commitment Task",
                                domain=[('is_expenditure', '=', False)]
                                )

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    is_expenditure = fields.Boolean(compute='_compute_is_expenditure',
                              string='Is Expenditure',
                              store=True)

    @api.one
    @api.depends('commitment_id')
    def _compute_is_expenditure(self):
        self.is_expenditure = bool(self.commitment_id)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    @api.onchange('is_expenditure')
    def _onchange_is_expenditure(self):
        if self.is_expenditure:
            self.project_id = self.commitment_id.project_id

    # CONSTRAINS
    # ----------------------------------------------------------
    # expenditure_ids exist in task model
    @api.one
    @api.constrains('is_expenditure')
    def _check_expenditure_ids(self):
        """
        Expenditure Can't have expenditure under
        """
        if self.is_expenditure and len(self.expenditure_ids) > 0:
            raise ValidationError("A Expenditure Task Can't have it's own Expenditure Task")

    # # total_expenditure_amount and total_commitment_amount
    # # exist in task
    # @api.one
    # @api.constrains('total_expenditure_amount', 'total_commitment_amount', 'is_expenditure')
    # def _check_total_expenditure_total_commitment(self):
    #     """
    #     The Total Expenditure must not be greater than Total Commitment
    #     If not expenditure
    #     """
    #     if not self.is_expenditure and self.total_expenditure_amount > self.total_commitment_amount:
    #         raise ValidationError("Commitment Task Total Expenditure Can't exceed Total Commitment")

