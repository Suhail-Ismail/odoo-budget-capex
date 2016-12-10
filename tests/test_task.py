# -*- coding: utf-8 -*-

from psycopg2._psycopg import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from faker import Faker

import random

fake = Faker()


class TaskTestCase(TransactionCase):
    at_install = False

    post_install = True

    def setUp(self):
        super(TaskTestCase, self).setUp()

    def test_uniqueness(self):
        """
        Checks if task is Unique
        """
        self.env['budget.capex.task'].create({
            'task_no': 'Task - 1'
        })

        with self.assertRaises(IntegrityError):
            self.env['budget.capex.task'].create({
                'task_no': 'Task - 1'
            })

    def test_is_child_or_is_parent_on_create(self):
        """
        Checks if task is child or parent when creating
        """

        task_1 = self.env['budget.capex.task'].create({
            'task_no': 'Task - 1',
        })

        task_2 = self.env['budget.capex.task'].create({
            'task_no': 'Task - 2',
            'parent_id': task_1.id
        })

        self.assertTrue(not task_1.is_child, "Task - 1 Must be Parent Task")
        self.assertTrue(task_2.is_child, "Task - 2 Must be Child Task")

    def test_is_child_or_is_parent_on_write(self):
        """
        Checks if task is child or parent when updating
        """

        task_1 = self.env['budget.capex.task'].create({
            'task_no': 'Task - 1'
        })

        task_2 = self.env['budget.capex.task'].create({
            'task_no': 'Task - 2',
            'parent_id': task_1.id
        })

        task_2.write(
            {
                'parent_id': False
            }
        )

        task_1.write(
            {
                'parent_id': task_2.id
            }
        )

        self.assertTrue(not task_2.is_child, "Task - 2 Must be Parent Task")
        self.assertTrue(task_1.is_child, "Task - 1 Must be Child Task")

    def test_total_expenditure_and_commitment(self):
        """
        Test the value of total expenditure
        """
        task = self.env['budget.capex.task'].create({
            'task_no': 'Total Task - 1',
            'commitment_amount': 1000,
            'expenditure_amount': 500,
        })

        self.assertTrue(task.total_commitment_amount == 0.00,
                        "Commitment {} is not 0.00".format(task.total_commitment_amount))
        self.assertTrue(task.total_expenditure_amount == 0.00,
                        "Expenditure {} is not 0.00".format(task.total_expenditure_amount))

        for workflow in ['process', 'authorize', 'close']:
            task.signal_workflow(workflow)
            self.assertTrue(task.total_commitment_amount == 1000,
                            "Commitment {} is not 1000".format(task.total_commitment_amount))
            self.assertTrue(task.total_expenditure_amount == 500,
                            "Expenditure {} is not 500".format(task.total_expenditure_amount))

        task_child = self.env['budget.capex.task'].create({
            'task_no': 'Total Task - 2',
            'commitment_amount': 1200,
            'expenditure_amount': 500,
            'parent_id': task.id
        })

        # TOTAL TASK - 1
        self.assertTrue(task.total_commitment_amount == 1000,
                        "Commitment {} is not 1000".format(task.total_commitment_amount))
        self.assertTrue(task.total_expenditure_amount == 500,
                        "Expenditure {} is not 500".format(task.total_expenditure_amount))

        # TOTAL TASK - 2
        self.assertTrue(task_child.total_commitment_amount == 0.00,
                        "Commitment {} is not 1000".format(task_child.total_commitment_amount))
        self.assertTrue(task_child.total_expenditure_amount == 0.00,
                        "Expenditure {} is not 500".format(task_child.total_expenditure_amount))

        for workflow in ['process', 'authorize', 'close']:
            task_child.signal_workflow(workflow)
            # TOTAL TASK - 1
            self.assertTrue(task.total_commitment_amount == 2200,
                            "Commitment {} is not 0.00".format(task.total_commitment_amount))
            self.assertTrue(task.total_expenditure_amount == 1000,
                            "Expenditure {} is not 0.00".format(task.total_expenditure_amount))

            # TOTAL TASK - 2
            self.assertTrue(task_child.total_commitment_amount == 1200,
                            "Commitment {} is not 1000".format(task_child.total_commitment_amount))
            self.assertTrue(task_child.total_expenditure_amount == 500,
                            "Expenditure {} is not 500".format(task_child.total_expenditure_amount))

    def test_is_child_onchange(self):
        region = self.env['budget.enduser.region'].create(
            {
                'name': 'Head Office',
                'alias': 'HO'
            }
        )
        project = self.env['budget.core.budget'].create(
            {
                'is_project': True,
                'region_id': region.id,
                'cwp': '1245',
                'category': 'C'
            }
        )


