# -*- coding: utf-8 -*-
{
    'name': "Capital Expenditure",
    'version': '0.1',
    'summary': 'CAPEX Management',
    'sequence': 3,
    'description': """
Odoo Module
===========
Specifically Designed for Etisalat-TBPC

CAPEX Management
---------------------
- Project
- Task
- Sub-task
- Accrual-CAPEX
- PCC

    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'document',
        'budget_contractor'
    ],
    'data': [
        'security/budget_capex.xml',
        'security/ir.model.access.csv',

        'views/task.xml',
        'views/project.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
