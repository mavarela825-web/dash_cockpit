from dash import html

def layout_context():
    return html.Div(
        [
            html.H2("Context", style={"color": "#ffffff"}),
            html.Div("Context page content goes here.", style={"color": "#ffffff"})
        ],
        style={"padding": "20px"}
    )
