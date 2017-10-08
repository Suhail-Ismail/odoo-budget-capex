# -*- coding: utf-8 -*-

from psycopg2._psycopg import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class CearTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(CearTestCase, self).setUp()
        self.project_id = self.env['budget.core.budget'].create({'project_no': 'sample cwp', 'is_project': True})
        self.division_id = self.env['budget.enduser.division'].create({'name': 'Division', 'alias': 'division'})
        self.section_id = self.env['budget.enduser.section'].create({'name': 'Section',
                                                                     'alias': 'section',
                                                                     'division_id': self.division_id.id})

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

    def test_total_pcc(self):
        cear_a = self.create_cear('Progress CEAR A', 100000.0, 0.0)
        cear_b = self.create_cear('Progress CEAR B', 10000.0, 0.0, cear_a.id)
        cear_c = self.create_cear('Progress CEAR C', 10000.0, 0.0, cear_a.id)
        cear_d = self.create_cear('Progress CEAR D', 10000.0, 0.0, cear_a.id)
        cear_e = self.create_cear('Progress CEAR E', 10000.0, 0.0, cear_d.id)
        cear_f = self.create_cear('Progress CEAR F', 10000.0, 0.0, cear_d.id)

        self.env['budget.capex.progress'].create({
            'progress_date': '2018-08-08',
            'project_id': self.project_id.id,
            'division_id': self.division_id.id,
            'section_id': self.section_id.id,
            'progress_line_ids': [
                (0, 0, {'cear_id': cear_f.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_f.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_f.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_e.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_e.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_e.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_d.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_d.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_d.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_c.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_c.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_c.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_b.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_b.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_b.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_a.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 4000.0}),
            ],
        })

        self.assertEqual(cear_f.total_pcc_amount, 15000.0)
        self.assertEqual(cear_e.total_pcc_amount, 15000.0)
        self.assertEqual(cear_d.total_pcc_amount, 45000.0)
        self.assertEqual(cear_c.total_pcc_amount, 15000.0)
        self.assertEqual(cear_b.total_pcc_amount, 15000.0)
        self.assertEqual(cear_a.total_pcc_amount, 90000.0)

    def test_percent_pcc(self):
        cear_a = self.create_cear('Percent PCC CEAR A', 100000.0, 100000.0)
        self.env['budget.capex.progress'].create({
            'progress_date': '2018-08-08',
            'project_id': self.project_id.id,
            'division_id': self.division_id.id,
            'section_id': self.section_id.id,
            'progress_line_ids': [
                (0, 0, {'cear_id': cear_a.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 4000.0}),
            ],
        })
        self.assertEqual(cear_a.percent_pcc, 15.0)

    def test_total_accrual(self):
        cear_a = self.create_cear('Accrual CEAR A', 100000.0, 0.0)
        cear_b = self.create_cear('Accrual CEAR B', 10000.0, 0.0, cear_a.id)
        cear_c = self.create_cear('Accrual CEAR C', 10000.0, 0.0, cear_a.id)
        cear_d = self.create_cear('Accrual CEAR D', 10000.0, 0.0, cear_a.id)
        cear_e = self.create_cear('Accrual CEAR E', 10000.0, 0.0, cear_d.id)
        cear_f = self.create_cear('Accrual CEAR F', 10000.0, 0.0, cear_d.id)

        self.env['budget.capex.accrual'].create({
            'accrual_date': '2018-08-08',
            'accrual_line_ids': [
                (0, 0, {'cear_id': cear_f.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_f.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_f.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_e.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_e.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_e.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_d.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_d.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_d.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_c.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_c.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_c.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_b.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_b.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_b.id, 'amount': 4000.0}),

                (0, 0, {'cear_id': cear_a.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 4000.0}),
            ],
        })

        self.assertEqual(cear_f.total_accrual_amount, 15000.0)
        self.assertEqual(cear_e.total_accrual_amount, 15000.0)
        self.assertEqual(cear_d.total_accrual_amount, 45000.0)
        self.assertEqual(cear_c.total_accrual_amount, 15000.0)
        self.assertEqual(cear_b.total_accrual_amount, 15000.0)
        self.assertEqual(cear_a.total_accrual_amount, 90000.0)

    def test_percent_accrual(self):
        cear_a = self.create_cear('Percent Accrual CEAR A', 100000.0, 100000.0)
        self.env['budget.capex.accrual'].create({
            'progress_date': '2018-08-08',
            'accrual_line_ids': [
                (0, 0, {'cear_id': cear_a.id, 'amount': 6000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 5000.0}),
                (0, 0, {'cear_id': cear_a.id, 'amount': 4000.0}),
            ],
        })
        self.assertEqual(cear_a.percent_accrual, 15.0)
