# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

from odoo.exceptions import UserError, ValidationError


class TaskChild(models.Model):
    _inherit = 'budget.capex.task'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    parent_id = fields.Many2one('budget.capex.task',
                                string="Parent Task",
                                domain=[('is_child', '=', False)]
                                )

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    is_child = fields.Boolean(compute='_compute_is_child',
                              string='Is Child',
                              store=True)

    @api.one
    @api.depends('parent_id')
    def _compute_is_child(self):
        self.is_child = bool(self.parent_id)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    @api.onchange('is_child')
    def _onchange_is_child(self):
        if self.is_child:
            self.project_id = self.parent_id.project_id

    # CONSTRAINS
    # ----------------------------------------------------------
    # child_ids exist in task model
    @api.one
    @api.constrains('is_child')
    def _check_child_ids(self):
        """
        Child Can't have child under
        """
        if self.is_child and len(self.child_ids) > 0:
            raise ValidationError("A Child Task Can't have it's own Child Task")

    # total_expenditure_amount and total_commitment_amount
    # exist in task
    @api.one
    @api.constrains('total_expenditure_amount', 'total_commitment_amount', 'is_child')
    def _check_total_expenditure_total_commitment(self):
        """
        The Total Expenditure must not be greater than Total Commitment
        If not child
        """
        if not self.is_child and self.total_expenditure_amount > self.total_commitment_amount:
            raise ValidationError("Parent Task Total Expenditure Can't exceed Total Commitment")

