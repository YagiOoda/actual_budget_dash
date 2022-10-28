
account_groups = {
    # Money that can only be touched for specific purposes, or by paying 
    # penalties/fees. 
    # Examples: Retirement Accounts, Health Saving or Spending Accounts, etc.
    'assets_restricted' : [
        "Roth IRA", "Vanguard 401k"
    ], 

    # Money that can become cash very quickly and without penalties. 
    # Examples: Checking, Savings, and Money Market Accounts.
    'assets_liquid' : [
        "Ally Savings", "Bank of America", "Capital One Checking"
    ], 

    # Non-tax deferred investment accounts, such as brokerage accounts.
    'assets_investment' : [
    ], 

    # House, Car, Jewlery, Artwork, etc.
    'assets_physical' : [
        "House Asset"
    ], 

    # Debts to be paid off over a long period of time and not tied to a 
    # physical asset
    # Examples: Student loans, personal loans, and collection accounts. Credit
    # cards are not included here.
    'liabilities_installment' : [
    ],

    # Debt carried on any physical assets listed in Assets-Physical.
    'liabilities_physical' : [
        "Mortgage"
    ],

    # Credit Cards that are not paid off at the end of the month and may 
    # accumulate interest.
    'liabilities_revolving' : [],

    # Credit Cards or Loans that are paid off every month.
    'liabilities_transacting' : [
        "HSBC"
    ], 
}

acct_group_sort = {
    'assets': [
        "assets_physical", "assets_restricted", "assets_investment", "assets_liquid"
    ],
    'debts': [
        "liabilities_physical", "liabilities_installment", "liabilities_revolving", "liabilities_transacting"
    ]
}

# Income off budget does not show in income accounts, this is to make the cashflow plots correct
cashflow_offbudget = {
    'offbudget_accts': [
        "Roth IRA", "Vanguard 401k", "House Asset", "Mortgage"
    ],
    'filter_payees': ["Starting Balance"],
}

# Filter out first month from cashflow calculations. This is useful if the first month of using Actual was a partial month.
cashflow_filter_first_mo = True
# Filter out current month from cashflow calculations. This is useful if the current month of Actual doesn't have any income/expenses yet.
cashflow_filter_current_mo = True

font_serif = "Proxima Nova"
font_mono = "Fira Code"