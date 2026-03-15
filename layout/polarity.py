from dash import html, dcc

POLARITY_OPTIONS = [
    {"label": "B", "value": "B"},
    {"label": "NB", "value": "NB"},
    {"label": "N", "value": "N"},
    {"label": "NB-", "value": "NB-"},
    {"label": "BR", "value": "BR"},
]

def polarity_row(tf, state):
    return html.Div(
        className="polarity-row",
        children=[
            html.Div(tf, className="tf-label"),
            dcc.RadioItems(
                id={"type": "polarity", "tf": tf},
                options=POLARITY_OPTIONS,
                value=state["polarity"][tf],
                className="polarity-control",
                inline=True
            )
        ]
    )
