import dash
from dash import html, dcc, Input, Output, callback

dash.register_page(__name__, path="/tick")

layout = html.Div(
    [
        html.H1("Tick Input", style={"color": "white"}),

        dcc.Input(
            id="tick-input",
            type="number",
            placeholder="Enter Tick Value",
            style={"marginBottom": "10px"},
        ),

        html.Button("Save Tick", id="save-tick", n_clicks=0),
        html.Button("Reset Tick", id="reset-tick", n_clicks=0, style={"marginLeft": "10px"}),

        html.Div(id="tick-status", style={"color": "white", "marginTop": "20px"}),
    ]
)

@callback(
    Output("tick-store", "data"),
    Output("tick-status", "children"),
    Input("save-tick", "n_clicks"),
    Input("reset-tick", "n_clicks"),
    Input("tick-input", "value"),
    prevent_initial_call=True,
)
def save_or_reset(save_clicks, reset_clicks, tick_value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, ""

    button = ctx.triggered[0]["prop_id"].split(".")[0]

    if button == "save-tick":
        return {"tick": tick_value}, f"Tick saved: {tick_value}"

    if button == "reset-tick":
        return {"tick": 0}, "Tick reset to 0"

    return dash.no_update, ""

@callback(
    Output("tick-input", "value"),
    Input("tick-store", "data"),
)
def load_saved_tick(data):
    if data and "tick" in data:
        return data["tick"]
    return 0