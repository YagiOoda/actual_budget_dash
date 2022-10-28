import dashboard.processing as proc
import utils.settings as config

ini = proc.read_actual_sql('data/db.sqlite')

## Find months in dataset
var = dict()
var['months'] = (ini['transactions']['date'].sort_values(ascending=True).dt.to_period('M')).unique()
var['account_groups'] = config.account_groups
var['acct_group_sort'] = config.acct_group_sort
var['filter_payee_id'] = ini['payees'][ini['payees']['name'].isin(config.cashflow_offbudget['filter_payees'])]['id']

## Filter transactions by account and by month
tx_by_acct = proc.get_tx_by_acct(ini, var)

## Filter transactions by category and by month
tx_by_cat = proc.get_tx_by_cat(ini, var)

## Filter categories by category group
cat_by_group = proc.get_cat_by_group(ini)

nw_by_mth = proc.get_nw_by_mth(ini, var, tx_by_acct)

cashflow_by_mth = proc.get_cashflow_by_mth(ini, var, tx_by_acct, tx_by_cat, cat_by_group, config)

#metrics = proc.get_metrics(var, nw_by_mth, cashflow_by_mth)