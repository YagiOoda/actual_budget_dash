import plotly.graph_objects as go         #to create interactive charts
from dash import html, dash_table, dcc
import numpy as np

import utils.settings as config


def fire_matrix_chart(var,metrics) -> dcc.Graph:
    fig = go.Figure()

    ## Add asset charts
    fig.add_trace(go.Scatter(
        x=metrics['savings_multiple']['6moMA'],
        y=metrics['savings_rate']['6moMA'],
        hovertemplate = '<b>%{text}</b>'+
                        '<br>Savings Rate: %{y:,.0%}'+
                        '<br>Savings Multiple: %{x:,.1f}',
        text = [var['months'][-len(metrics['savings_multiple']['6moMA']):][i].strftime("%b %Y") for i in range(len(metrics['savings_multiple']['6moMA']))],
        name='',
        mode='lines+markers', 
        showlegend=False,
    ))

    fig.add_vline(x=25,line_width=3, line_dash="dash")

    fig.update_xaxes(
        range=[0,30],
    )

    fig.update_yaxes(
        range=[0,1],
        tickformat=',.0%',
    )
    fig.update_layout(
        title="<b>FIRE Matrix</b>",
        xaxis_title="Savings Multiple",
        yaxis_title="Savings Rate",
        margin = dict(t=40, l=0, r=0, b=0),
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family= config.font_mono,
            size=14,
        ),
    )

    fig.add_annotation(
        text="Accumulation<br>Phase",
        font=dict(
            size=16,
        ),
        hovertext="https://minafi.com/fire-matrix",
        xref="x", yref="paper",
        align="right",
        xanchor="right",
        yanchor="top",
        x=25, y=1, showarrow=False
    )

    fig.add_annotation(
        text="Financial<br>Independence<br>& Income",
        font=dict(
            size=16,
        ),
        hovertext="https://minafi.com/fire-matrix",
        xref="paper", yref="paper",
        align="right",
        xanchor="right",
        yanchor="top",
        x=1, y=1, showarrow=False
    )

    return dcc.Graph(
        id='fire_matrix',
        figure=fig,
        style={
            'height': '40vh',
        }
    )

def withdrawal_rate_chart(var,config, metrics) -> dcc.Graph:
    fig = go.Figure()

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
    else:
        months = var['months']

    if config.cashflow_filter_current_mo == True:
        months = months[:-1]

    ## Add asset charts
    fig.add_trace(go.Scatter(
        x=months.to_timestamp(),
        y=metrics['withdrawal_rate']['monthly'],
        #hovertemplate = '<b>%{text}</b>'+
        #                '<br>Savings Rate: %{y:,.0%}'+
        #                '<br>Savings Multiple: %{x:,.1f}',
        name='Withdrawal Rate',
        mode='lines+markers', 
    ))

    fig.add_trace(go.Scatter(
        x=months[-len(metrics['withdrawal_rate']['6moMA']):].to_timestamp(),
        y=metrics['withdrawal_rate']['6moMA'],
        #hovertemplate = '<b>%{text}</b>'+
        #                '<br>Savings Rate: %{y:,.0%}'+
        #                '<br>Savings Multiple: %{x:,.1f}',
        name='6-mo WR',
        mode='lines+markers', 
    ))

    if len(metrics['withdrawal_rate']['12moMA']) != 0:
        fig.add_trace(go.Scatter(
            x=months[-len(metrics['withdrawal_rate']['12moMA']):].to_timestamp(),
            y=metrics['withdrawal_rate']['12moMA'],
            #hovertemplate = '<b>%{text}</b>'+
            #                '<br>Savings Rate: %{y:,.0%}'+
            #                '<br>Savings Multiple: %{x:,.1f}',
            name='12-mo WR',
            mode='lines+markers', 
        ))
        

    fig.update_layout(
        title="<b>Withdrawal Rate Over Time</b>",
        xaxis_title="Month",
        yaxis_title="Withdrawal Rate",
        margin = dict(t=40, l=0, r=0, b=0),
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family=config.font_mono,
            size=14,
        ),
    )
    
    fig.update_yaxes(tickformat=',.1%')

    fig.update_xaxes(tickformat='%b %Y')

    return dcc.Graph(
        id='withdrawal_rate',
        figure=fig,
        style={
            'height': '40vh',
        }
    )

def spending_chart(var,config, cashflow_by_mth) -> dcc.Graph:
    fig = go.Figure()

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
    else:
        months = var['months']

    if config.cashflow_filter_current_mo == True:
        months = months[:-1]

    ## Add asset charts
    fig.add_trace(go.Scatter(
        x=months.to_timestamp(),
        y=-1*np.array(cashflow_by_mth['expenses']),
        #hovertemplate = '<b>%{text}</b>'+
        #                '<br>Savings Rate: %{y:,.0%}'+
        #                '<br>Savings Multiple: %{x:,.1f}',
        name='Expenses',
        mode='lines+markers', 
    ))

    fig.add_trace(go.Scatter(
        x=months[-len(cashflow_by_mth['expenses_6moMA']):].to_timestamp(),
        y=-1*np.array(cashflow_by_mth['expenses_6moMA']),
        #hovertemplate = '<b>%{text}</b>'+
        #                '<br>Savings Rate: %{y:,.0%}'+
        #                '<br>Savings Multiple: %{x:,.1f}',
        name='6-mo Expenses',
        mode='lines+markers', 
    ))

    if len(cashflow_by_mth['expenses_12moMA']) != 0:
        fig.add_trace(go.Scatter(
            x=months[-len(cashflow_by_mth['expenses_12moMA']):].to_timestamp(),
            y=-1*np.array(cashflow_by_mth['expenses_12moMA']),
            #hovertemplate = '<b>%{text}</b>'+
            #                '<br>Savings Rate: %{y:,.0%}'+
            #                '<br>Savings Multiple: %{x:,.1f}',
            name='12-mo Expenses',
            mode='lines+markers', 
        ))
        
    fig.update_xaxes(tickformat='%b %Y')

    fig.update_layout(
        title="<b>Spending Over Time</b>",
        xaxis_title="Month",
        yaxis_title="Expenses",
        margin = dict(t=40, l=0, r=0, b=0),
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family=config.font_mono,
            size=14,
        ),
    )

    return dcc.Graph(
        id='expenses',
        figure=fig,
        style={
            'height': '40vh',
        }
    )

def savings_rate_chart(var,config, metrics) -> dcc.Graph:
    fig = go.Figure()

    if config.cashflow_filter_first_mo == True:
        months = var['months'][1:]
    else:
        months = var['months']

    if config.cashflow_filter_current_mo == True:
        months = months[:-1]

    ## Add asset charts
    fig.add_trace(go.Scatter(
        x=months.to_timestamp(),
        y=metrics['savings_rate']['monthly'],
        name='Savings Rate',
        mode='lines+markers', 
    ))

    fig.add_trace(go.Scatter(
        x=months[-len(metrics['savings_rate']['6moMA']):].to_timestamp(),
        y=metrics['savings_rate']['6moMA'],
        name='6-mo Savings Rate',
        mode='lines+markers', 
    ))

    if len(metrics['savings_rate']['12moMA']) != 0:
        fig.add_trace(go.Scatter(
            x=months[-len(metrics['savings_rate']['12moMA']):].to_timestamp(),
            y=metrics['savings_rate']['12moMA'],
            name='12-mo Savings Rate',
            mode='lines+markers', 
        ))
        
    fig.update_yaxes(tickformat=',.1%')

    fig.update_xaxes(tickformat='%b %Y')

    fig.update_layout(
        title="<b>Savings Rate Over Time</b>",
        xaxis_title="Month",
        yaxis_title="Savings Rate",
        margin = dict(t=40, l=0, r=0, b=0),
        title_font=dict(
            family=config.font_serif,
            size=18,
        ),
        font=dict(
            family=config.font_mono,
            size=14,
        ),
    )

    return dcc.Graph(
        id='expenses',
        figure=fig,
        style={
            'height': '40vh',
        }
    )
