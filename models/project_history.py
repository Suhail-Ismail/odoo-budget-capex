# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _
from .utils import choices_tuple

class ProjectHistory(models.Model):
    _name = 'budget.project.history'
    _description = 'Project History'

    # CHOICES
    # ----------------------------------------------------------
    OPTIONS = choices_tuple(['add', 'subtract', 'transfer'], is_sorted=False)


    # BASIC FIELDS
    # ----------------------------------------------------------
    option = fields.Selection(string='Option', selection=OPTIONS)
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Expenditure Amount')
    change_date = fields.Date(string="Change Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    project_id = fields.Many2one('budget.project', string="Project No")
    from_project_id = fields.Many2one('budget.project',
                                      string="From Project No")
    to_project_id = fields.Many2one('budget.project',
                                    string="To Project No")

    # CONSTRAINS
    # ----------------------------------------------------------
    @api.one
    @api.constrains('option', 'project_id', 'from_project_id', 'to_project_id')
    def _check_option(self):
        if self.option == 'transfer' and self.from_project_id == self.to_project_id:
            raise ValidationError(_("Transfer Option: From and To Project should not be equal"))

        elif self.option == 'transfer' and self.project_id.project_no not in [self.to_project_id.project_no,
                                                                              self.to_project_id.project_no]:
            raise ValidationError(_("Transfer Option: Transfer is invalid %s must be in from or to" % self.project_id.project_no))

    @api.onchange('option', 'project_id', 'from_project_id', 'to_project_id', 'commitment_amount', 'expenditure_amount')
    def onchange_option(self):
        if self.option == 'add':
            self.commitment_amount *= -1 if self.commitment_amount < 0 else 1
            self.expenditure_amount *= -1 if self.expenditure_amount < 0 else 1

        elif self.option == 'subtract':
            self.commitment_amount *= -1 if self.commitment_amount > 0 else 1
            self.expenditure_amount *= -1 if self.expenditure_amount > 0 else 1

        elif self.option == 'transfer':
            self.commitment_amount = abs(self.commitment_amount)
            self.expenditure_amount = abs(self.expenditure_amount)

            self.commitment_amount *= -1 if self.project_id.project_no == self.from_project_id.project_no else 1
            self.expenditure_amount *= -1 if self.project_id.project_no == self.from_project_id.project_no else 1
