import dash
from dash import html

dash.register_page(__name__, path="/context")

layout = html.Div(
    [html.H1("Context Page", style={"color": "white"})]
)