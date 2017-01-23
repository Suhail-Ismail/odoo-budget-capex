# -*- coding: utf-8 -*-

from psycopg2._psycopg import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from faker import Faker

import random

fake = Faker()


class CearTestCase(TransactionCase):
    at_install = False

    post_install = True

    def setUp(self):
        super(CearTestCase, self).setUp()

    def test_uniqueness(self):
        """
        Checks if cear is Unique
        """
        self.env['budget.capex.cear'].create({
            'cear_no': 'Cear - 1'
        })

        with self.assertRaises(IntegrityError):
            self.env['budget.capex.cear'].create({
                'cear_no': 'Cear - 1'
            })

    # def test_is_child_or_is_parent_on_create(self):
    #     """
    #     Checks if cear is child or parent when creating
    #     """
    #
    #     cear_1 = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Cear - 1',
    #     })
    #
    #     cear_2 = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Cear - 2',
    #         'parent_id': cear_1.id
    #     })
    #
    #     self.assertTrue(not cear_1.is_child, "Cear - 1 Must be Parent Cear")
    #     self.assertTrue(cear_2.is_child, "Cear - 2 Must be Child Cear")
    #
    # def test_is_child_or_is_parent_on_write(self):
    #     """
    #     Checks if cear is child or parent when updating
    #     """
    #
    #     cear_1 = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Cear - 1'
    #     })
    #
    #     cear_2 = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Cear - 2',
    #         'parent_id': cear_1.id
    #     })
    #
    #     cear_2.write(
    #         {
    #             'parent_id': False
    #         }
    #     )
    #
    #     cear_1.write(
    #         {
    #             'parent_id': cear_2.id
    #         }
    #     )
    #
    #     self.assertTrue(not cear_2.is_child, "Cear - 2 Must be Parent Cear")
    #     self.assertTrue(cear_1.is_child, "Cear - 1 Must be Child Cear")
    #
    # def test_total_expenditure_and_commitment(self):
    #     """
    #     Test the value of total expenditure
    #     """
    #     cear = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Total Cear - 1',
    #         'commitment_amount': 1000,
    #         'expenditure_amount': 500,
    #     })
    #
    #     self.assertTrue(cear.total_commitment_amount == 0.00,
    #                     "Commitment {} is not 0.00".format(cear.total_commitment_amount))
    #     self.assertTrue(cear.total_expenditure_amount == 0.00,
    #                     "Expenditure {} is not 0.00".format(cear.total_expenditure_amount))
    #
    #     for workflow in ['process', 'authorize', 'close']:
    #         cear.signal_workflow(workflow)
    #         self.assertTrue(cear.total_commitment_amount == 1000,
    #                         "Commitment {} is not 1000".format(cear.total_commitment_amount))
    #         self.assertTrue(cear.total_expenditure_amount == 500,
    #                         "Expenditure {} is not 500".format(cear.total_expenditure_amount))
    #
    #     cear_child = self.env['budget.capex.cear'].create({
    #         'cear_no': 'Total Cear - 2',
    #         'commitment_amount': 1200,
    #         'expenditure_amount': 500,
    #         'parent_id': cear.id
    #     })
    #
    #     # TOTAL TASK - 1
    #     self.assertTrue(cear.total_commitment_amount == 1000,
    #                     "Commitment {} is not 1000".format(cear.total_commitment_amount))
    #     self.assertTrue(cear.total_expenditure_amount == 500,
    #                     "Expenditure {} is not 500".format(cear.total_expenditure_amount))
    #
    #     # TOTAL TASK - 2
    #     self.assertTrue(cear_child.total_commitment_amount == 0.00,
    #                     "Commitment {} is not 1000".format(cear_child.total_commitment_amount))
    #     self.assertTrue(cear_child.total_expenditure_amount == 0.00,
    #                     "Expenditure {} is not 500".format(cear_child.total_expenditure_amount))
    #
    #     for workflow in ['process', 'authorize', 'close']:
    #         cear_child.signal_workflow(workflow)
    #         # TOTAL TASK - 1
    #         self.assertTrue(cear.total_commitment_amount == 2200,
    #                         "Commitment {} is not 0.00".format(cear.total_commitment_amount))
    #         self.assertTrue(cear.total_expenditure_amount == 1000,
    #                         "Expenditure {} is not 0.00".format(cear.total_expenditure_amount))
    #
    #         # TOTAL TASK - 2
    #         self.assertTrue(cear_child.total_commitment_amount == 1200,
    #                         "Commitment {} is not 1000".format(cear_child.total_commitment_amount))
    #         self.assertTrue(cear_child.total_expenditure_amount == 500,
    #                         "Expenditure {} is not 500".format(cear_child.total_expenditure_amount))
    #
    # def test_is_child_onchange(self):
    #     region = self.env['budget.enduser.region'].create(
    #         {
    #             'name': 'Head Office',
    #             'alias': 'HO'
    #         }
    #     )
    #     project = self.env['budget.core.budget'].create(
    #         {
    #             'is_project': True,
    #             'region_id': region.id,
    #             'cwp': '1245',
    #             'category': 'C'
    #         }
    #     )
    #
    #
