from dash import html, dcc
import dash

dash.register_page(__name__, path="/tick")

layout = html.Div(
    [
        html.H2("Tick Controls", style={"color": "#ffffff", "textAlign": "center"}),

        html.Div(
            [
                html.Label("Tick Value", style={"color": "#ffffff"}),

                dcc.Slider(
                    id="tick-slider",
                    min=-1200,
                    max=1200,
                    step=10,
                    value=0,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),

                dcc.Input(
                    id="tick-input",
                    type="number",
                    min=-1200,
                    max=1200,
                    step=10,
                    value=0,
                    style={"width": "120px", "marginTop": "15px"},
                ),
            ],
            style={"padding": "20px"},
        ),

        # No Apply button needed anymore
    ]
)
