import dash
from dash import html
import dashboard.pages.metrics.metrics_layout as metrics_layout
import dashboard.pages.metrics.metrics_ini as metrics_ini

dash.register_page(__name__, path="/metrics")

header = html.H3('Welcome to metrics!')


layout = html.Div([
        # top row
        html.Div([
            # summary table
            metrics_layout.fire_matrix_chart(metrics_ini.var, metrics_ini.metrics),
        ]),
        html.Div([
            # summary table
            metrics_layout.withdrawal_rate_chart(metrics_ini.var, metrics_ini.config, metrics_ini.metrics),
        ]),
        html.Div([
            # summary table
            metrics_layout.spending_chart(metrics_ini.var, metrics_ini.config, metrics_ini.cashflow_by_mth)
        ]),
        html.Div([
            # summary table
            metrics_layout.savings_rate_chart(metrics_ini.var, metrics_ini.config, metrics_ini.metrics)
        ]),
    ])

#layout = html.Div([
#    header,
#])
