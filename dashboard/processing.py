import sqlite3 as sql
import pandas as pd
import numpy as np
import utils.settings as config
from utils.functions import moving_average

def read_actual_sql(db):
    ini = dict()

    con = sql.connect(db)
    ini['transactions'] = pd.read_sql("SELECT id,acct,category,amount,description,notes,date,transferred_id FROM transactions WHERE tombstone = 0 AND isParent=0", con)
    ini['accounts'] = pd.read_sql("SELECT id,name,type,offbudget,closed,tombstone FROM accounts WHERE tombstone = 0", con)
    ini['categories'] = pd.read_sql("SELECT id,name,is_income,cat_group FROM categories WHERE tombstone = 0", con)
    ini['category_groups'] = pd.read_sql("SELECT id,name,is_income FROM category_groups WHERE tombstone = 0", con)
    ini['payees'] = pd.read_sql("SELECT id,name from payees WHERE tombstone=0", con)
    con.close()

    ini['transactions']['date'] = pd.to_datetime(ini['transactions']['date'], format='%Y%m%d')
    pd.set_option('display.max_rows', 1000)
    return ini

def get_tx_by_acct(ini,var):
    tx_by_acct = dict()

    for id in ini['accounts']['id'].tolist():
        tx_by_acct[id] = dict()
        tx_by_acct[id]['all'] = ini['transactions'][ini['transactions']['acct'] == id]
        tx_by_acct[id]['sum'] = []
        for month in var['months']:
            tx_by_acct[id][month] = tx_by_acct[id]['all'][tx_by_acct[id]['all']['date'].dt.to_period('M') == month]
            tx_by_acct[id]['sum'].append(tx_by_acct[id][month]['amount'].sum())

    for key in var['account_groups'].keys():
        check = all(item in ini['accounts']['name'].tolist() for item in var['account_groups'][key])
        if check == False:
            print('Review names')

    ini['accounts']['name'].tolist()

    return tx_by_acct

def get_tx_by_cat(ini,var):
    tx_by_cat = dict()

    for id in ini['categories']['id'].tolist():
        tx_by_cat[id] = dict()
        tx_by_cat[id]['all'] = ini['transactions'][ini['transactions']['category'] == id]
        tx_by_cat[id]['sum'] = []
        for month in var['months']:
            tx_by_cat[id][month] = tx_by_cat[id]['all'][tx_by_cat[id]['all']['date'].dt.to_period('M') == month]
            tx_by_cat[id]['sum'].append(tx_by_cat[id][month]['amount'].sum())

    return tx_by_cat


def get_cat_by_group(ini):
    cat_by_group = dict()
    for cat in ini['category_groups']['id'].tolist():
        cat_by_group[cat] = ini['categories'][ini['categories']['cat_group'] == cat]
    
    return cat_by_group

def get_nw_by_mth(ini, var, tx_by_acct):
    nw_by_mth = {key:[] for key in var['account_groups']}
    nw_by_mth['all'] = []
    nw_by_mth['assets'] = []
    nw_by_mth['debts'] = []
    for i in range(len(var['months'])):
        nw_by_mth['all'].append(0)
        nw_by_mth['assets'].append(0)
        nw_by_mth['debts'].append(0)
        for group in var['account_groups']:
            accounts = ini['accounts'][ini['accounts']['name'].isin(var['account_groups'][group])]
            nw_by_mth[group].append(0)
            for account in accounts['id']:
                nw_by_mth[group][i] += tx_by_acct[account][var['months'][i]]['amount'].sum()/100
            if i != 0:
                nw_by_mth[group][i] += nw_by_mth[group][i-1]
            nw_by_mth['all'][i] += nw_by_mth[group][i]
            if group[0] == 'a':
                nw_by_mth['assets'][i] += nw_by_mth[group][i]
            else:
                nw_by_mth['debts'][i] += nw_by_mth[group][i]
    
    return nw_by_mth

def get_cashflow_by_mth(ini, var, tx_by_acct, tx_by_cat, cat_by_group, config):
    # TODO: add in config to filter out first month

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
    else:
        months = var['months']
    
    if config.cashflow_filter_current_mo == True:
        months = months[:-1]

    cashflow_by_mth = {key:[] for key in ini['category_groups']['id']}
    cashflow_by_mth['income'] = []
    cashflow_by_mth['income_pre_tax'] = []
    cashflow_by_mth['expenses'] = []
    cashflow_by_mth['diff'] = []
    for i in range(len(months)):
        cashflow_by_mth['income'].append(0)
        cashflow_by_mth['income_pre_tax'].append(0)
        cashflow_by_mth['expenses'].append(0)
        for group in ini['category_groups']['id']:
            categories = cat_by_group[group]
            cashflow_by_mth[group].append(0)
            for cat in categories['id']:
                txns = tx_by_cat[cat][months[i]]
                txns = txns[txns['transferred_id'].isnull()]
                cashflow_by_mth[group][i] += txns[~txns['description'].isin(var['filter_payee_id'].tolist())]['amount'].sum()/100
            if (categories['is_income'] == 1).all():
                cashflow_by_mth['income'][i] += cashflow_by_mth[group][i]
            else:
                cashflow_by_mth['expenses'][i] += cashflow_by_mth[group][i]
        # Start going through retirement accounts for income
        for account in config.cashflow_offbudget['offbudget_accts']:
            txns = tx_by_acct[ini['accounts'][ini['accounts']['name']==account]['id'].to_string(index=False)][months[i]]
            txns = txns[txns['transferred_id'].isnull()]
            cashflow_by_mth['income_pre_tax'][i] += txns[~txns['description'].isin(var['filter_payee_id'].tolist())]['amount'].sum()/100
        cashflow_by_mth['income'][i] += cashflow_by_mth['income_pre_tax'][i]
        cashflow_by_mth['diff'].append(cashflow_by_mth['income'][i]+cashflow_by_mth['expenses'][i])
        
    cashflow_by_mth['category_groups'] = ini['category_groups']

    # Calculate 6 and 12 month moving averages for different spending category groups
    for group in ini['category_groups']['id']:
        cashflow_by_mth[(group+'_6moMA')] = moving_average(cashflow_by_mth[group],6)

    cashflow_by_mth['income_6moMA'] = moving_average(cashflow_by_mth['income'],6)
    cashflow_by_mth['income_12moMA'] = moving_average(cashflow_by_mth['income'],12)
    cashflow_by_mth['income_pre_tax_6moMA'] = moving_average(cashflow_by_mth['income_pre_tax'],6)
    cashflow_by_mth['income_pre_tax_12moMA'] = moving_average(cashflow_by_mth['income_pre_tax'],12)
    cashflow_by_mth['expenses_6moMA'] = moving_average(cashflow_by_mth['expenses'],6)
    cashflow_by_mth['expenses_12moMA'] = moving_average(cashflow_by_mth['expenses'],12)
    cashflow_by_mth['diff_6moMA'] = moving_average(cashflow_by_mth['diff'],6)
    cashflow_by_mth['diff_12moMA'] = moving_average(cashflow_by_mth['diff'],12)
    
    return cashflow_by_mth


def get_metrics(var, nw_by_mth, cashflow_by_mth):
    #Savings Rate, Withdrawal Rate, Savings Multiple, 6mo ma, 12mo ma

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
        first_mo_offset = 1
    else:
        months = var['months']
        first_mo_offset = 0

    if config.cashflow_filter_current_mo == True:
        months = months[:-1]
        last_mo_offset = -1
    else:
        last_mo_offset = None


    metrics = dict()
    ## Savings Rate = 1-expenses/income
    metrics['savings_rate'] = dict()
    metrics['savings_rate']['monthly']=1+np.array(cashflow_by_mth['expenses'])/np.array(cashflow_by_mth['income'])
    metrics['savings_rate']['6moMA'] = 1+cashflow_by_mth['expenses_6moMA']/cashflow_by_mth['income_6moMA']
    metrics['savings_rate']['12moMA'] = 1+cashflow_by_mth['expenses_12moMA']/cashflow_by_mth['income_12moMA']

    ## Withdrawal Rate = expenses/(net worth - property)
    metrics['withdrawal_rate'] = dict()
    metrics['withdrawal_rate']['monthly'] = -1*np.array(cashflow_by_mth['expenses'])/(np.array(nw_by_mth['all'][first_mo_offset:last_mo_offset])-np.array(nw_by_mth['assets_physical'][first_mo_offset:last_mo_offset]))
    try:
        metrics['withdrawal_rate']['6moMA'] = -1*cashflow_by_mth['expenses_6moMA']/(np.array(nw_by_mth['all'][-1*len(cashflow_by_mth['expenses_6moMA'])::])-np.array(nw_by_mth['assets_physical'][-1*len(cashflow_by_mth['expenses_6moMA'])::]))
    except: metrics['withdrawal_rate']['6moMA'] = []
    try:
        metrics['withdrawal_rate']['12moMA'] = -1*cashflow_by_mth['expenses_12moMA']/(np.array(nw_by_mth['all'][-1*len(cashflow_by_mth['expenses_12moMA'])::])-np.array(nw_by_mth['assets_physical'][-1*len(cashflow_by_mth['expenses_12moMA'])::]))
    except: metrics['withdrawal_rate']['12moMA'] = []

    ## Savings Multiple = (net worth - property)/(expenses*12)
    metrics['savings_multiple'] = dict()
    metrics['savings_multiple']['monthly'] = (np.array(nw_by_mth['all'][first_mo_offset:last_mo_offset])-np.array(nw_by_mth['assets_physical'][first_mo_offset:last_mo_offset]))/(-1*np.array(cashflow_by_mth['expenses'])*12)
    try:
        metrics['savings_multiple']['6moMA'] = (np.array(nw_by_mth['all'][-1*len(cashflow_by_mth['expenses_6moMA'])::])-np.array(nw_by_mth['assets_physical'][-1*len(cashflow_by_mth['expenses_6moMA'])::]))/(-1*cashflow_by_mth['expenses_6moMA']*12)
    except: metrics['savings_multiple']['6moMA'] = []
    try:
        metrics['savings_multiple']['12moMA'] = (np.array(nw_by_mth['all'][-1*len(cashflow_by_mth['expenses_12moMA'])::])-np.array(nw_by_mth['assets_physical'][-1*len(cashflow_by_mth['expenses_12moMA'])::]))/(-1*cashflow_by_mth['expenses_12moMA']*12)
    except: metrics['savings_multiple']['12moMA'] = []
    
    return metrics
