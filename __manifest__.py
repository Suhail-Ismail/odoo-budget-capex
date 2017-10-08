# -*- coding: utf-8 -*-
{
    'name': "Capital Expenditure",
    'version': '0.1',
    'summary': 'CAPEX Management',
    'sequence': 4,
    'description': """
Budget Capital Expenditure
===========
Specifically Designed for Etisalat-TBPC

Summary
---------------------
- Project Inherit
    - Added Cear Detail (ie. Total Commitment/Expenditure/Accrual/Progress/Balance)
- Cear Commitment
- Cear Expenditure
- Cear Progress
- Cear Progress/Accrual
- Access Users
    - Cear
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Cear Progress/Accrual
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
- Validation
    - Cear No must be unique
    - Cear Expenditure can't have it's own child cear
    - Cear Commitment Total Expenditure amount can't be greater than Total Commitment amount
    - Individual Progress can't be greater than 100%
    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'budget_core'
    ],
    'data': [
        'security/budget_capex.xml',
        'security/ir.model.access.csv',

        'views/cear.xml',
        'views/progress.xml',
        'views/progress_line.xml',
        'views/accrual.xml',

        'views/contract_inherit.xml',
        'views/budget_inherit.xml',

        'workflows/budget_capex_cear.xml',

        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
