# -*- coding: utf-8 -*-

from psycopg2._psycopg import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from faker import Faker

import random


class CearTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(CearTestCase, self).setUp()

    def create_cear(self, no='', commitment_amount=0.0, expenditure_amount=0.0, parent_id=False):
        return self.env['budget.capex.cear'].create({
            'no': no,
            'commitment_amount': commitment_amount,
            'expenditure_amount': expenditure_amount,
            'parent_id': parent_id
        })

    def test_constraint_exp_less_or_eq_commitment_01(self):
        with self.assertRaises(IntegrityError):
            self.create_cear('exp_less_or_eq_commitment A', 10000.0, 1000000.0)

    def test_constraint_exp_less_or_eq_commitment_02(self):
        cear_b = self.create_cear('exp_less_or_eq_commitment B', 10000.0, 1000.0)
        self.create_cear('exp_less_or_eq_commitment B-1', 0.0, 1000.0, cear_b.id)
        self.create_cear('exp_less_or_eq_commitment B-2', 0.0, 1000.0, cear_b.id)

        with self.assertRaises(IntegrityError):
            self.create_cear('exp_less_or_eq_commitment B-3', 0.0, 1000000.0, cear_b.id)

    def test_total_commitment(self):
        # A
        commitment_a = self.create_cear('Commitment A', 5000.0, 0.0, False)

        # A LEVEL 1
        commitment_a_1 = self.create_cear('Commitment A-1', 1000.0, 0.0, commitment_a.id)
        commitment_a_2 = self.create_cear('Commitment A-2', 2000.0, 0.0, commitment_a.id)
        commitment_a_3 = self.create_cear('Commitment A-3', 3000.0, 0.0, commitment_a.id)

        # A LEVEL 2
        self.create_cear('Commitment A-1-1', 1000.0, 0.0, commitment_a_1.id)
        self.create_cear('Commitment A-1-2', 2000.0, 0.0, commitment_a_1.id)
        self.create_cear('Commitment A-1-3', 3000.0, 0.0, commitment_a_1.id)

        self.create_cear('Commitment A-2-1', 1000.0, 0.0, commitment_a_2.id)
        self.create_cear('Commitment A-2-2', 2000.0, 0.0, commitment_a_2.id)
        self.create_cear('Commitment A-2-3', 3000.0, 0.0, commitment_a_2.id)

        self.create_cear('Commitment A-3-1', 1000.0, 0.0, commitment_a_3.id)
        self.create_cear('Commitment A-3-2', 2000.0, 0.0, commitment_a_3.id)
        self.create_cear('Commitment A-3-3', 3000.0, 0.0, commitment_a_3.id)

        # B
        commitment_b = self.create_cear('Commitment B', 5000.0, 0.0, False)

        # B LEVEL 1
        commitment_b_1 = self.create_cear('Commitment B-1', 1000.0, 0.0, commitment_b.id)
        commitment_b_2 = self.create_cear('Commitment B-2', 2000.0, 0.0, commitment_b.id)
        commitment_b_3 = self.create_cear('Commitment B-3', 3000.0, 0.0, commitment_b.id)

        # B LEVEL 2
        self.create_cear('Commitment B-1-1', 1000.0, 0.0, commitment_b_1.id)
        self.create_cear('Commitment B-1-2', 2000.0, 0.0, commitment_b_1.id)
        self.create_cear('Commitment B-1-3', 3000.0, 0.0, commitment_b_1.id)

        self.create_cear('Commitment B-2-1', 1000.0, 0.0, commitment_b_2.id)
        self.create_cear('Commitment B-2-2', 2000.0, 0.0, commitment_b_2.id)
        self.create_cear('Commitment B-2-3', 3000.0, 0.0, commitment_b_2.id)

        self.create_cear('Commitment B-3-1', 1000.0, 0.0, commitment_b_3.id)
        self.create_cear('Commitment B-3-2', 2000.0, 0.0, commitment_b_3.id)
        self.create_cear('Commitment B-3-3', 3000.0, 0.0, commitment_b_3.id)

        self.assertEqual(commitment_a.total_commitment_amount, 29000)
        self.assertEqual(commitment_b.total_commitment_amount, 29000)

    def test_total_expenditure(self):
        # A
        expenditure_a = self.create_cear('Expenditure A', 30000.0, 5000.0, False)

        # A LEVEL 1
        expenditure_a_1 = self.create_cear('Expenditure A-1', 30000.0, 1000.0, expenditure_a.id)
        expenditure_a_2 = self.create_cear('Expenditure A-2', 30000.0, 2000.0, expenditure_a.id)
        expenditure_a_3 = self.create_cear('Expenditure A-3', 30000.0, 3000.0, expenditure_a.id)

        # A LEVEL 2
        self.create_cear('Expenditure A-1-1', 30000.0, 1000.0, expenditure_a_1.id)
        self.create_cear('Expenditure A-1-2', 30000.0, 2000.0, expenditure_a_1.id)
        self.create_cear('Expenditure A-1-3', 30000.0, 3000.0, expenditure_a_1.id)

        self.create_cear('Expenditure A-2-1', 30000.0, 1000.0, expenditure_a_2.id)
        self.create_cear('Expenditure A-2-2', 30000.0, 2000.0, expenditure_a_2.id)
        self.create_cear('Expenditure A-2-3', 30000.0, 3000.0, expenditure_a_2.id)

        self.create_cear('Expenditure A-3-1', 30000.0, 1000.0, expenditure_a_3.id)
        self.create_cear('Expenditure A-3-2', 30000.0, 2000.0, expenditure_a_3.id)
        self.create_cear('Expenditure A-3-3', 30000.0, 3000.0, expenditure_a_3.id)

        # B
        expenditure_b = self.create_cear('Expenditure B', 30000.0, 5000.0, False)

        # B LEVEL 1
        expenditure_b_1 = self.create_cear('Expenditure B-1', 30000.0, 1000.0, expenditure_b.id)
        expenditure_b_2 = self.create_cear('Expenditure B-2', 30000.0, 2000.0, expenditure_b.id)
        expenditure_b_3 = self.create_cear('Expenditure B-3', 30000.0, 3000.0, expenditure_b.id)

        # B LEVEL 2
        self.create_cear('Expenditure B-1-1', 30000.0, 1000.0, expenditure_b_1.id)
        self.create_cear('Expenditure B-1-2', 30000.0, 2000.0, expenditure_b_1.id)
        self.create_cear('Expenditure B-1-3', 30000.0, 3000.0, expenditure_b_1.id)

        self.create_cear('Expenditure B-2-1', 30000.0, 1000.0, expenditure_b_2.id)
        self.create_cear('Expenditure B-2-2', 30000.0, 2000.0, expenditure_b_2.id)
        self.create_cear('Expenditure B-2-3', 30000.0, 3000.0, expenditure_b_2.id)

        self.create_cear('Expenditure B-3-1', 30000.0, 1000.0, expenditure_b_3.id)
        self.create_cear('Expenditure B-3-2', 30000.0, 2000.0, expenditure_b_3.id)
        self.create_cear('Expenditure B-3-3', 30000.0, 3000.0, expenditure_b_3.id)

        self.assertEqual(expenditure_a.total_expenditure_amount, 29000.0)
        self.assertEqual(expenditure_b.total_expenditure_amount, 29000.0)
