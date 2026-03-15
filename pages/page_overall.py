import dash
from dash import html, dcc

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H1("Overall Picture", style={"color": "white"}),
        html.Div(id="overall-content"),
    ]
)

def layout_overall(tick_value):
    normalized = (tick_value + 1000) / 2000
    normalized = max(0, min(1, normalized))

    return html.Div(
        [
            html.H3(f"Current Tick: {tick_value}", style={"color": "white"}),

            dcc.Graph(
                id="tick-meter",
                figure={
                    "data": [
                        {
                            "type": "indicator",
                            "mode": "gauge+number",
                            "value": tick_value,
                            "gauge": {
                                "axis": {"range": [-1000, 1000]},
                                "bar": {"color": "#00FFAA"},
                                "bgcolor": "#111111"},
                        }
                    ],
                    "layout": {
                        "paper_bgcolor": "#000000",
                        "plot_bgcolor": "#000000",
                        "height": 300,
                    },
                },
            ),
        ]
    )