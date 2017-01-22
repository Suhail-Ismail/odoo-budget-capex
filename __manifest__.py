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
    - Added Task Detail (ie. Total Commitment/Expenditure/Accrual/Progress/Balance)
- Task Commitment
- Task Expenditure
- Task Progress
- Task Progress/Accrual
- Access Users
    - Task
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Task Progress/Accrual
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
- Validation
    - Task No must be unique
    - Task Expenditure can't have it's own child task
    - Task Commitment Total Expenditure amount can't be greater than Total Commitment amount
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

        'views/task_commitment.xml',
        'views/task_expenditure.xml',
        'views/progress.xml',

        'views/budget_inherit.xml',

        'workflows/budget_capex_task.xml',

        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
