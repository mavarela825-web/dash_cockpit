from dash import html

def layout_bias():
    return html.Div(
        [
            html.H2("Bias", style={"color": "#ffffff"}),
            html.Div("Bias page content goes here.", style={"color": "#ffffff"})
        ],
        style={"padding": "20px"}
    )
