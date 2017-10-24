# -*- coding: utf-8 -*-

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

    def create_cear(self, no='', commitment_amount=0.0, expenditure_amount=0.0,
                    parent_id=False, real_cear_id=False):
        return self.env['budget.capex.cear'].create({
            'input_no': no,
            'input_commitment_amount': commitment_amount,
            'input_expenditure_amount': expenditure_amount,
            'parent_id': parent_id,
            'real_cear_id': real_cear_id,
        })

    # def test_constraint_exp_less_or_eq_commitment_01(self):
    #     with self.assertRaises(IntegrityError):
    #         self.create_cear('exp_less_or_eq_commitment A', 10000.0, 1000000.0)
    #
    # def test_constraint_exp_less_or_eq_commitment_02(self):
    #     cear_b = self.create_cear('exp_less_or_eq_commitment B', 10000.0, 1000.0)
    #     self.create_cear('exp_less_or_eq_commitment B-1', 0.0, 1000.0, cear_b.id)
    #     self.create_cear('exp_less_or_eq_commitment B-2', 0.0, 1000.0, cear_b.id)
    #
    #     with self.assertRaises(IntegrityError):
    #         self.create_cear('exp_less_or_eq_commitment B-3', 0.0, 1000000.0, cear_b.id)

    def test_no(self):
        # TODO
        pass

    def test_unique_identifier_related(self):
        cear_a = self.create_cear("RELATED CEAR A", 10000, 5000)
        cear_b = self.create_cear("RELATED CEAR B", 10000, 5000, cear_a.id)

        self.assertEqual(cear_b.unique_identifier, 'Related:RELATED CEAR B')

    def test_unique_identifier_virtual(self):
        cear_a = self.create_cear("RELATED CEAR A", 10000, 5000)
        cear_b = self.create_cear("RELATED CEAR B", 10000, 5000)
        cear_c = self.create_cear("RELATED CEAR C", 10000, 5000, cear_a.id, cear_b.id)

        self.assertEqual(cear_c.unique_identifier, 'Virtual:RELATED CEAR B:RELATED CEAR A')

    def test_unique_identifier_distributed(self):
        cear_a = self.env['budget.capex.cear'].create({
            'input_no': "DISTRIBUTED CEAR A",
            'input_commitment_amount': 10000,
            'input_expenditure_amount': 5000,
            'has_distribution': True})

        self.assertEqual(cear_a.unique_identifier, 'Distributed:DISTRIBUTED CEAR A')

    def test_unique_identifier_main(self):
        cear_a = self.create_cear("MAIN CEAR A", 10000, 5000)
        self.assertEqual(cear_a.unique_identifier, 'Main:MAIN CEAR A')

    def test_group(self):
        cear_a = self.create_cear("GROUP CEAR A", 10000, 5000)
        cear_b = self.create_cear("GROUP CEAR B", 10000, 5000, cear_a.id)
        cear_c = self.create_cear("GROUP CEAR C", 10000, 5000, cear_b.id)
        cear_d = self.create_cear("GROUP CEAR D", 10000, 5000, cear_c.id)

        self.assertEqual(cear_a.group_id.id, cear_a.id)
        self.assertEqual(cear_b.group_id.id, cear_a.id)
        self.assertEqual(cear_c.group_id.id, cear_a.id)
        self.assertEqual(cear_d.group_id.id, cear_a.id)
