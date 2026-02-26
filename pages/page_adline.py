from dash import html

def layout_adline():
    return html.Div(
        [
            html.H2("AD Line", style={"color": "#ffffff"}),
            html.Div("AD Line page content goes here.", style={"color": "#ffffff"})
        ],
        style={"padding": "20px"}
    )
