import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go         #to create interactive charts

from dash import html, dash_table, dcc
from dash.dash_table import DataTable, FormatTemplate
from collections import OrderedDict

import utils.settings as config



def summary_table(nw_by_mth):

    data = OrderedDict([
        ('left', ["Assets", "Debts", "Net Worth"]),
        ('right', [round(nw_by_mth['assets'][-1],2), nw_by_mth['debts'][-1], nw_by_mth['all'][-1]]),
    ])
    df = pd.DataFrame(data)

    fig = dash_table.DataTable(
        columns = [
            {'name': "Balances", 'id': 'left'},
            {'name': "Balances", 'id': 'right', 'type': 'numeric', 'format': FormatTemplate.money(2)},
        ],
        data=df.to_dict('records'),
        merge_duplicate_headers=True,
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font_size': '16px',
            'font_family': config.font_serif,
        },
        style_cell_conditional=[
            {
                'if': {'column_id':'left'},
                'textAlign': 'left'
            }
        ],
        style_data_conditional=[
            {
            'if': {'row_index':3},
            'border-top': 'solid 2px #CCC'
            }
        ],
        style_data = {
                'font_family': config.font_mono,
                'font_size': '14px',
        },
    )
    
    return fig

def cashflow_table(cashflow_by_mth):

    data = OrderedDict([
        ('left', ["Cashflow (6 mo MA)", "Expenses (6 mo MA)"]),
        ('right', [round(cashflow_by_mth['diff_6moMA'][-1],2), (-1*cashflow_by_mth['expenses_6moMA'][-1])]),
    ])
    df = pd.DataFrame(data)

    fig = dash_table.DataTable(
        columns = [
            {'name': "Cashflow", 'id': 'left'},
            {'name': "Cashflow", 'id': 'right', 'type': 'numeric', 'format': FormatTemplate.money(2)},
        ],
        data=df.to_dict('records'),
        merge_duplicate_headers=True,
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font_size': '16px',
            'font_family': config.font_serif,
        },
        style_cell_conditional=[
            {
                'if': {'column_id':'left'},
                'textAlign':'left'
            },
            {
                'if': {'column_id':'left'},
                'font_family': config.font_serif
            }
        ],
        style_data = {
                'font_family': config.font_mono,
                'font_size': '14px',
        },
    )
    return fig

def fire_table(cashflow_by_mth, nw_by_mth):

    data = OrderedDict([
        ('left', ["","Lean FI/RE", "FI/RE", "Fat FI/RE"]),
        ('amount', ["Amount [$]", -1*(cashflow_by_mth['expenses_6moMA'][-1]*12/0.04),
            -1*(cashflow_by_mth['expenses_6moMA'][-1]*12/0.03),
            -1*(cashflow_by_mth['expenses_6moMA'][-1]*12/0.02)]),
        ('time', ["Time [Y]", round(npf.nper(0.06/12, -1*cashflow_by_mth['diff_6moMA'][-1],-1*nw_by_mth['all'][-1], -1*cashflow_by_mth['expenses_6moMA'][-1]*12/0.04, 1)/12,2),
            round(npf.nper(0.06/12, -1*cashflow_by_mth['diff_6moMA'][-1],-1*nw_by_mth['all'][-1], -1*cashflow_by_mth['expenses_6moMA'][-1]*12/0.03, 1)/12,2),
            round(npf.nper(0.06/12, -1*cashflow_by_mth['diff_6moMA'][-1],-1*nw_by_mth['all'][-1], -1*cashflow_by_mth['expenses_6moMA'][-1]*12/0.02, 1)/12,2)
            ]),
        ('right', ["", "", "", ""]),

    ])
    df = pd.DataFrame(data)

    fig = dash_table.DataTable(
        columns = [
            {"name": "FI/RE - Current Expenses", "id": "left"},
            {"name": "FI/RE - Current Expenses", "id": "amount", "type": "numeric", "format": FormatTemplate.money(2)},
            {"name": "FI/RE - Current Expenses", "id": "time"},
        ],
        data=df.to_dict('records'),
        merge_duplicate_headers=True,
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font_size': '16px',
            'font_family': config.font_serif,
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'left'},
                'textAlign': 'left'
            },
            {
                'if': {'column_id': 'left'},
                'font_family': config.font_serif
            }
        ],
        style_data = {
                'font_family': config.font_mono,
                'font_size': '14px',
                'height': '1vh',
        },
        style_data_conditional = [
            {
                "if": {"row_index": 0},
                "fontWeight": "bold",
                'textAlign': "center",
                'font_family': config.font_serif,
            },
            #{
            #   Future work, make the amount be a data bar 
            #   https://dash.plotly.com/datatable/conditional-formatting#displaying-data-bars
            #   data_bars(df, 'lifeExp')
            #},
        ],
        css=[{"selector": ".dash-table-container tr", 
         "rule":'max-height: "10px"; height: "10px"; '}],
    )

    return fig

def networth_graph(nw_by_mth, ini_accounts, var) -> dcc.Graph:

    fig = go.Figure()

    ## Add asset charts
    fig.add_trace(go.Scatter(
        x=var['months'].to_timestamp(),
        y=nw_by_mth['all'],
        hoverinfo='y', 
        hoveron = 'points', 
        hovertemplate = '%{y:$,.2f}',
        mode='lines+markers', 
        name='Sum'
    ))

    for i in range(len(var['acct_group_sort']['assets'])):
        fig.add_trace(go.Scatter(
            x=var['months'].to_timestamp(), 
            y=nw_by_mth[var['acct_group_sort']['assets'][i]], 
            hoverinfo='y', 
            hoveron = 'points+fills', 
            hovertemplate = '%{y:$,.2f}',
            mode='lines+markers', 
            stackgroup = "one",
            legendgroup="assets",legendgrouptitle_text="Assets",
            legendrank= i,
            name= var['acct_group_sort']['assets'][i].replace('_', ': ').title()
        )) 

    for i in range(len(var['acct_group_sort']['debts'])):
        fig.add_trace(go.Scatter(
            x=var['months'].to_timestamp(), 
            y=nw_by_mth[var['acct_group_sort']['debts'][i]], 
            hoverinfo='y', 
            hoveron = 'points+fills', 
            hovertemplate = '%{y:$,.2f}',
            mode='lines+markers', 
            stackgroup = "two",
            legendgroup="debts", 
            legendgrouptitle_text= "Debts",
            legendrank=(len(var['acct_group_sort']['debts'])-i),
            name= var['acct_group_sort']['debts'][i].replace('_', ': ').title(),
        )) 
    
    fig.update_layout(
        title="<b>Net Worth</b>",
        #xaxis_title="Date",
        yaxis_title="Amount",
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family=config.font_mono,
            size=14,
        ),
        margin=dict(t=40, l=40, r=0, b=0),
        hovermode='x unified',
    )

    fig.update_xaxes(
        hoverformat='%b %Y',
    )

    return dcc.Graph(
        id='net_worth',
        figure=fig,
        style={
            'height': '45vh',
        }
    )

def cashflow_graph(cashflow_by_mth, var) -> dcc.Graph:

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
    else:
        months = var['months']

    if config.cashflow_filter_current_mo == True:
        months = months[:-1]

    fig = go.Figure()
    fig.add_bar(
        name='Income',
        x=months.to_timestamp(),
        y=cashflow_by_mth['income'],
        hovertemplate = '%{y:$,.2f}',
        legendrank=1,
        base=0,
    )
    fig.add_bar(
        name='Expenses',
        x=months.to_timestamp(),
        y=cashflow_by_mth['expenses'],
        hovertemplate = '%{y:$,.2f}',
        legendrank=2,
        base=0,
    )
    fig.update_layout(barmode='stack')
    fig.add_trace(go.Scatter(
        x=months.to_timestamp(), 
        y=cashflow_by_mth['diff'],
        hoverinfo='y', 
        hovertemplate = '%{y:$,.2f}',
        mode='lines+markers', 
        name='Cashflow'))

    fig.update_layout(
        title="<b>Cashflow</b>",
        #xaxis_title="Date",
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        yaxis_title="Amount",
        font=dict(
            family=config.font_mono,
            size=14,
        ),
        margin = dict(t=40, l=0, r=0, b=40),
        legend_traceorder = 'normal',
        hovermode='x unified',
        hoverlabel=dict(
            font_family= config.font_serif
        ),
    )

    fig.update_xaxes(
        hoverformat='%b %Y',
    )

    return dcc.Graph(
        id='cashflow',
        figure=fig,
        style={
            'height': '40vh',
        },
    )

def savings_rate_piechart(var,cashflow_by_mth) -> dcc.Graph:

    # Savings labels and values
    savings_parent = ['6-mo<br>Cashflow', 'Savings','Savings']
    savings_lab = ['Savings', 'Post-tax','Pre-tax']
    savings_vals = [cashflow_by_mth['diff_6moMA'][-1],cashflow_by_mth['diff_6moMA'][-1]-cashflow_by_mth['income_pre_tax_6moMA'][-1],cashflow_by_mth['income_pre_tax_6moMA'][-1]]

    # Expenses labels and values
    expenses_parent = ["6-mo<br>Cashflow", "Expenses", "Expenses", "Expenses", "Expenses", "Expenses"]
    expenses_lab = ['Expenses']
    expenses_lab.extend(cashflow_by_mth['category_groups']['name'][cashflow_by_mth['category_groups']['is_income'] != 1].tolist())

    tmp_vals = []
    for group in cashflow_by_mth['category_groups']['id'][cashflow_by_mth['category_groups']['is_income'] != 1]:
        tmp_vals.append(round(cashflow_by_mth[(group+'_6moMA')][-1]*-1,2))
    expenses_vals = [sum(tmp_vals)]
    expenses_vals.extend(tmp_vals)

    parent_lab = savings_parent + expenses_parent
    lab = savings_lab+expenses_lab
    vals = savings_vals+expenses_vals

    fig =go.Figure(go.Sunburst(
        labels=lab,
        parents=parent_lab,
        values=vals,
        branchvalues="total",
        hoverinfo="percent entry+label",
        rotation=90,
    ))

    fig.update_layout(
        margin = dict(t=40, l=0, r=0, b=0),
        #title = "<b>6-mo Average Monthly Cashflow</b>",
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family=config.font_serif,
            size=14,
        ),
    )

    return dcc.Graph(
        id='cash_flow',
        figure=fig,
        style={
            'height': '40vh',
        }
    )

