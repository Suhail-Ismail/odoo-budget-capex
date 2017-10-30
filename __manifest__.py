# -*- coding: utf-8 -*-
{
    'name': "Capital Expenditure",
    'version': '11.0.0.1',
    'summary': 'CAPEX Management',
    'sequence': 4,
    'description': """
    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'budget_enduser',
        'budget_core',
        'budget_contractor'
    ],
    'data': [
        'security/budget_capex.xml',
        'security/ir.model.access.csv',

        'views/cear.xml',
        'views/progress.xml',
        'views/progress_line.xml',
        'views/accrual.xml',
        'views/accrual_line.xml',

        'views/contract_inherit.xml',
        'views/budget_inherit.xml',

        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
