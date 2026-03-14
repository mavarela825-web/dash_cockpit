import dash
from dash import html

dash.register_page(__name__, path="/adline")

layout = html.Div(
    [html.H1("AD Line Page", style={"color": "white"})]
)