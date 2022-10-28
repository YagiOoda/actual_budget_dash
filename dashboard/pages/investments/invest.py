import dash
from dash import html, callback, Input, Output
import dashboard.pages.investments.invest_ini as invest_ini
import dashboard.pages.investments.invest_layout as invest_layout

from dash import html, dash_table, dcc


dash.register_page(__name__, path="/invest")

header = html.H3('Welcome to page 2!')


accounts = invest_ini.var['account_groups']['assets_investment']
accounts.extend(invest_ini.var['account_groups']['assets_restricted'])

layout = html.Div([
        dcc.Dropdown(
            accounts,
            accounts,
            id='investment-dropdown',
            multi=True,
        ),
        html.Div(
            id='dd-investment-chart',
        ),
    ])

#layout = html.Div([
#    header,
#])

@callback(
    Output('dd-investment-chart', 'children'),
    Input('investment-dropdown', 'value')
)
def update_output(selection):
    return invest_layout.investments_chart(invest_ini.var, invest_ini.config, selection, invest_ini.ini, invest_ini.tx_by_acct, invest_ini.nw_by_mth)
