
def investments_chart(var,config,selection, ini, tx_by_acct, nw_by_mth):

    if config.cashflow_filter_first_mo == True:
        if config.cashflow_filter_current_mo == True:
            months = var['months'][1:-1]
        else:
            months = var['months'][1:]
    else:
        months = var['months']
    
    txns_by_mth = []
    total_by_mth = []
    #for i in range(len(months)):
    #    txns_by_mth.append(None)
    #    total_by_mth.append(None)
    #    for sel in selection:
    #        txns = tx_by_acct[ini['accounts'][ini['accounts']['name']==sel]['id'].to_string(index=False)][months[i]]
    #        # Find transactions that aren't the end of the month balance or starting balance
    #        txns_by_mth[i] += txns[~txns['description'].isin(var['filter_payee_id'].tolist())][['date','amount']]
    #        total_by_mth[i] += txns[txns['description'].isin(var['filter_payee_id'].tolist())][['date','amount']]

    return f'You have selected {selection}'