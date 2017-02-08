Budget Capital Expenditure
===========
Specifically Designed for Etisalat-TBPC

Summary
---------------------
- Project Inherit
    - Added Cear Detail (ie. Total Commitment/Expenditure/Accrual/Progress/Balance)
- Cear Parent
- Cear Child
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
    - Cear Child can't have it's own child cear
    - Cear Parent Total Expenditure amount can't be greater than Total Commitment amount
    - Individual Progress can't be greater than 100%