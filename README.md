Budget Capital Expenditure
===========
Specifically Designed for Etisalat-TBPC

Summary
---------------------
- Project Inherit
    - Added Task Detail (ie. Total Commitment/Expenditure/Accrual/Progress/Balance)
- Task Parent
- Task Child
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
    - Task Child can't have it's own child task
    - Task Parent Total Expenditure amount can't be greater than Total Commitment amount
    - Individual Progress can't be greater than 100%