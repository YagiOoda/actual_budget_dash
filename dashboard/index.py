from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dashboard.layout.navbar import create_navbar
#from dashboard.pages.investments.invest_callbacks


# Toggle the themes at [dbc.themes.LUX]
# The full list of available themes is:
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, PULSE, SANDSTONE,
# SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI.
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.LUX],
    use_pages=True)

nav = create_navbar()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.P(),
    dash.page_container
])

