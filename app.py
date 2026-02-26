from dash import Dash, html, dcc, Input, Output, State
import dash

from pages.page_overall import layout_overall

app = Dash(__name__, use_pages=True)
server = app.server

# ---------------------------------------------------------
# MAIN APP LAYOUT WITH PERMANENT SIDEBAR
# ---------------------------------------------------------
app.layout = html.Div(
    [
        # SIDEBAR (always visible)
        html.Div(
            [
                html.H2("Cockpit", style={"color": "white", "textAlign": "center"}),

                dcc.Link("Overall Picture", href="/", style={"display": "block", "color": "white", "margin": "10px"}),
                dcc.Link("Context", href="/context", style={"display": "block", "color": "white", "margin": "10px"}),
                dcc.Link("Bias", href="/bias", style={"display": "block", "color": "white", "margin": "10px"}),
                dcc.Link("Tick", href="/tick", style={"display": "block", "color": "white", "margin": "10px"}),
                dcc.Link("AD Line", href="/adline", style={"display": "block", "color": "white", "margin": "10px"}),
            ],
            style={
                "width": "220px",
                "backgroundColor": "#111111",
                "padding": "20px",
                "height": "100vh",
                "position": "fixed",
                "left": 0,
                "top": 0,
            },
        ),

        # MAIN CONTENT AREA
        html.Div(
            [
                html.Div(id="overall-content"),
                dash.page_container,
                dcc.Store(id="tick-store", storage_type="local"),
            ],
            style={"marginLeft": "240px", "padding": "20px"},
        ),
    ]
)

# ---------------------------------------------------------
# SYNC SLIDER <-> INPUT (LIVE)
# ---------------------------------------------------------
@app.callback(
    Output("tick-input", "value"),
    Output("tick-slider", "value"),
    Input("tick-slider", "value"),
    Input("tick-input", "value"),
)
def sync_tick_controls(slider_val, input_val):
    ctx = dash.callback_context

    if not ctx.triggered:
        return input_val, slider_val

    trigger = ctx.triggered[0]["prop_id"]

    if "tick-slider" in trigger:
        return slider_val, slider_val

    if "tick-input" in trigger:
        return input_val, input_val

    return input_val, slider_val


# ---------------------------------------------------------
# LIVE UPDATE: STORE TICK VALUE AUTOMATICALLY
# ---------------------------------------------------------
@app.callback(
    Output("tick-store", "data"),
    Input("tick-slider", "value"),
)
def live_save_tick(tick_value):
    return {"tick": tick_value}


# ---------------------------------------------------------
# UPDATE OVERALL PAGE GAUGE
# ---------------------------------------------------------
@app.callback(
    Output("overall-content", "children"),
    Input("tick-store", "data"),
)
def display_overall(data):
    tick_value = 0
    if data and "tick" in data:
        tick_value = data["tick"]

    return layout_overall(tick_value)


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
