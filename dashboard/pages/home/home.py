import dash
from dash import html
import dashboard.pages.home.home_layout as home_layout
import dashboard.pages.home.home_ini as home_ini

dash.register_page(__name__, path='/')

header = html.H3('Welcome to home page!')

layout = html.Div([
    # top row
    html.Div([
        # summary table
        html.Div([
            home_layout.summary_table(home_ini.nw_by_mth),
            home_layout.cashflow_table(home_ini.cashflow_by_mth),
            home_layout.fire_table(home_ini.cashflow_by_mth, home_ini.nw_by_mth)
        ],className="three columns"),
        # networth graph
        html.Div([
            home_layout.networth_graph(home_ini.nw_by_mth, home_ini.ini['accounts'], home_ini.var)
        ],className="nine columns"),
    ]),
    # bottom row
    html.Div([
        html.Div([
            home_layout.cashflow_graph(home_ini.cashflow_by_mth, home_ini.var)
        ], className="nine columns"),
        html.Div([
            home_layout.savings_rate_piechart(home_ini.var, home_ini.cashflow_by_mth)
        ], className="three columns")
    ]),
])

#layout = html.Div([
#    header,
#])
