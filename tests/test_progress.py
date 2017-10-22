# -*- coding: utf-8 -*-

from psycopg2._psycopg import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from faker import Faker

import random


class ProgressTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(ProgressTestCase, self).setUp()
        self.project_id = self.env['budget.core.budget'].create({'project_no': 'sample cwp', 'is_project': True})
        self.division_id = self.env['budget.enduser.division'].create({'name': 'Division', 'alias': 'division'})
        self.section_id = self.env['budget.enduser.section'].create({'name': 'Section',
                                                                     'alias': 'section',
                                                                     'division_id': self.division_id.id})

    def create_progress(self, received_date=False, project_id=False, division_id=False, section_id=False):
        section_id = self.section_id.id if not section_id else section_id.id
        division_id = self.division_id.id if not division_id else division_id.id
        project_id = self.project_id.id if not project_id else project_id.id
        received_date = '1990-01-01' if not received_date else received_date

        return self.env['budget.capex.progress'].create({
            'received_date': received_date,
            'project_id': project_id,
            'division_id': division_id,
            'section_id': section_id
        })

    def test_generate_reference_no(self):
        pcc = self.create_progress('2017-01-01')
        self.assertEqual(pcc.reference_no, 'section-2017-001')

        pcc = self.create_progress('2017-01-01')
        self.assertEqual(pcc.reference_no, 'section-2017-002')

        pcc = self.create_progress('2017-01-01')
        self.assertEqual(pcc.reference_no, 'section-2017-003')

        pcc = self.create_progress('2017-01-01')
        self.assertEqual(pcc.reference_no, 'section-2017-004')

        pcc = self.create_progress('2018-01-01')
        self.assertEqual(pcc.reference_no, 'section-2018-001')

        pcc = self.create_progress('2018-01-01')
        self.assertEqual(pcc.reference_no, 'section-2018-002')

        section_id = self.env['budget.enduser.section'].create({'name': 'Section1',
                                                                'alias': 'section1',
                                                                'division_id': self.division_id.id})

        pcc = self.create_progress(received_date='2017-01-01', section_id=section_id)
        self.assertEqual(pcc.reference_no, 'section1-2017-001')

        pcc = self.create_progress(received_date='2017-01-01', section_id=section_id)
        self.assertEqual(pcc.reference_no, 'section1-2017-002')

        pcc = self.create_progress(received_date='2018-01-01', section_id=section_id)
        self.assertEqual(pcc.reference_no, 'section1-2018-001')
