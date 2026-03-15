# app.py
"""
Dash app with a single writer for dcc.Store(id="context-store").
Save this file as app.py and run with: python .\app.py
"""

import dash
from dash import Dash, html, dcc, Input, Output, State, no_update
from datetime import datetime

# -------------------------
# Configuration / thresholds
# -------------------------
MAX_RANGE = 2000

# -------------------------
# Helper: color selection based on tick
# -------------------------
def pick_colors_for_tick(tick):
    """
    Color mapping rules (updated):
    - Positive side:
      * 1..599 -> very light green
      * 600..700 -> light green shade
      * 800..900 -> medium green
      * 1000..2000 -> strong green
      * other positive -> bright green
    - Negative side:
      * -1..-599 -> lightest red
      * 600..700 (abs) -> light red shade
      * 800..900 (abs) -> medium red
      * 1000..2000 (abs) -> strong red
      * other negative -> bright red
    - tick == None -> neutral greys
    - tick == 0 -> neutral center (no active side)
    """
    neutral_left = "#5a5a5a"
    neutral_right = "#5a5a5a"

    if tick is None:
        return neutral_left, neutral_right

    # Positive side (tick > 0)
    if tick > 0:
        # very light for small positive values
        if 1 <= tick <= 599:
            right_color = "#e8fff0"  # very light green
        elif 600 <= tick <= 700:
            right_color = "#b7f5c9"
        elif 800 <= tick <= 900:
            right_color = "#66e07a"
        elif 1000 <= tick <= 2000:
            right_color = "#00c853"
        else:
            right_color = "#00ff66"
        left_color = "#111111"
        return left_color, right_color

    # Negative side (tick < 0)
    if tick < 0:
        a = abs(tick)
        # lightest red for small negative values
        if 1 <= a <= 599:
            left_color = "#ffecec"  # lightest red
        elif 600 <= a <= 700:
            left_color = "#f5b7b7"
        elif 800 <= a <= 900:
            left_color = "#e06666"
        elif 1000 <= a <= 2000:
            left_color = "#c62828"
        else:
            left_color = "#ff4d4d"
        right_color = "#111111"
        return left_color, right_color

    # tick == 0 (neutral)
    return "#111111", "#00ff66"

# -------------------------
# Tick circle figure
# -------------------------
def make_full_circle_figure(tick):
    if tick is None:
        left_active = 0
        right_active = 0
    else:
        left_active = abs(min(0, tick))
        right_active = max(0, tick)
    left_rest = max(0, MAX_RANGE - left_active)
    right_rest = max(0, MAX_RANGE - right_active)
    values = [left_active, left_rest, right_active, right_rest]
    left_color, right_color = pick_colors_for_tick(tick)
    if tick is None:
        colors = ["#5a5a5a", "#2a2a2a", "#5a5a5a", "#2a2a2a"]
        center_text = "—"
    else:
        colors = [left_color, "#111111", right_color, "#111111"]
        center_text = str(tick)
    fig = {
        "data": [
            {
                "type": "pie",
                "values": values,
                "marker": {"colors": colors, "line": {"width": 0}},
                "hole": 0.60,
                "rotation": 90,
                "direction": "clockwise",
                "sort": False,
                "textinfo": "none",
                "hoverinfo": "none",
                "showlegend": False,
                "domain": {"x": [0, 1], "y": [0, 1]},
            }
        ],
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "height": 360,
            "margin": {"t": 10, "b": 10, "l": 10, "r": 10},
            "annotations": [
                {
                    "text": center_text,
                    "x": 0.5,
                    "y": 0.48,
                    "showarrow": False,
                    "font": {"size": 36, "color": "white", "family": "Arial"},
                }
            ],
        },
    }
    return fig

# -------------------------
# Sentiments and colors
# -------------------------
SENTIMENTS = [
    ("bullish", "Bullish"),
    ("bullish_neutral", "Bullish Neutral"),
    ("neutral", "Neutral"),
    ("neutral_bearish", "Neutral Bearish"),
    ("bearish", "Bearish"),
]

BUTTON_COLORS = {
    "bullish": {"bg": "#003d1a", "border": "#00c853", "text": "#b7f5c9"},
    "bullish_neutral": {"bg": "#0b2f18", "border": "#66e07a", "text": "#bfeecf"},
    "neutral": {"bg": "#1f1f1f", "border": "#888888", "text": "#cccccc"},
    "neutral_bearish": {"bg": "#2f1a1a", "border": "#e06666", "text": "#f5c6c6"},
    "bearish": {"bg": "#2a0f0f", "border": "#c62828", "text": "#f5b7b7"},
}

# Card header colors requested by user
CARD_HEADER_COLORS = {
    "overnight": "#8e44ad",       # Purple
    "bigger": "#ff8c42",          # Orange
    "intermediate": "#ff6fa3",    # Pink
    "shortterm": "#89cff0",       # Baby blue
}

# -------------------------
# Styles and sizes
# -------------------------
LEFT_PANEL_WIDTH = 320
RIGHT_PANEL_WIDTH = 420
CARD_GRAPH_HEIGHT = 360

BASE_CARD_STYLE = {
    "background": "rgba(20,20,20,0.6)",
    "padding": "10px",
    "borderRadius": "8px",
    "border": "1px solid rgba(255,255,255,0.03)",
    "marginBottom": "10px",
}

BUTTON_BASE_STYLE = {
    "width": "100%",
    "textAlign": "left",
    "padding": "8px 10px",
    "marginBottom": "6px",
    "borderRadius": "6px",
    "border": "1px solid rgba(255,255,255,0.06)",
    "background": "transparent",
    "color": "#ddd",
    "cursor": "pointer",
    "boxSizing": "border-box",
}

CARD_HEADER_STYLE = {
    "fontSize": "14px",
    "color": "#ddd",
    "marginBottom": "8px",
    "textAlign": "left",
    "fontWeight": "700",
    "display": "flex",
    "alignItems": "center",
    "gap": "8px",
}

# -------------------------
# App and layout
# -------------------------
app = Dash(__name__)
server = app.server

def make_sentiment_buttons(card_name):
    buttons = []
    for val, label in SENTIMENTS:
        btn_id = f"{card_name}-btn-{val}"
        buttons.append(
            html.Button(
                label,
                id=btn_id,
                n_clicks=0,
                style={**BUTTON_BASE_STYLE},
            )
        )
    return buttons

def make_card_header(card_key, title_text):
    """
    Create a header with a full-width colored top bar and colored title text.
    card_key must be one of the keys in CARD_HEADER_COLORS.
    """
    color = CARD_HEADER_COLORS.get(card_key, "#888888")
    top_bar = html.Div(style={
        "height": "8px",
        "background": color,
        "borderTopLeftRadius": "6px",
        "borderTopRightRadius": "6px",
        "margin": "-10px -10px 8px -10px",  # extend to card edges
    })
    title = html.Div(title_text, style={
        "fontSize": "14px",
        "color": color,
        "marginBottom": "6px",
        "textAlign": "left",
        "fontWeight": "700",
        "paddingLeft": "4px",
    })
    return html.Div([top_bar, title])

app.layout = html.Div(
    style={"backgroundColor": "#000000", "minHeight": "100vh", "color": "white", "fontFamily": "Arial"},
    children=[
        dcc.Store(id="op-state", data={"tick": None, "history": []}),
        dcc.Store(id="context-store", data={"overnight": None, "bigger_picture": None, "intermediate": None, "shortterm": None}),

        # Left context panel
        html.Div(
            id="left-context-panel",
            role="region",
            **{"aria-label": "Context panel"},
            style={
                "position": "fixed",
                "top": "24px",
                "left": "0px",
                "width": f"{LEFT_PANEL_WIDTH}px",
                "zIndex": 99999,
                "background": "linear-gradient(180deg, rgba(28,28,28,0.98), rgba(22,22,22,0.98))",
                "padding": "12px",
                "borderTopRightRadius": "10px",
                "borderBottomRightRadius": "10px",
                "borderRight": "1px solid rgba(255,255,255,0.04)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.6)",
                "maxHeight": "92vh",
                "overflowY": "auto",
            },
            children=[
                html.Div("Context", style={"fontSize": "16px", "color": "#ddd", "marginBottom": "10px", "fontWeight": "700"}),

                html.Div(
                    id="card-overnight",
                    children=[make_card_header("overnight", "Overnight"), *make_sentiment_buttons("overnight")],
                    style=BASE_CARD_STYLE,
                ),

                html.Div(
                    id="card-bigger",
                    children=[make_card_header("bigger", "Bigger Picture"), *make_sentiment_buttons("bigger")],
                    style=BASE_CARD_STYLE,
                ),

                html.Div(
                    id="card-intermediate",
                    children=[make_card_header("intermediate", "Intermediate"), *make_sentiment_buttons("intermediate")],
                    style=BASE_CARD_STYLE,
                ),

                html.Div(
                    id="card-shortterm",
                    children=[make_card_header("shortterm", "Shortterm"), *make_sentiment_buttons("shortterm")],
                    style=BASE_CARD_STYLE,
                ),
            ],
        ),

        # Main content padding
        html.Div(id="main-content", style={"padding": "24px", "paddingLeft": f"{LEFT_PANEL_WIDTH + 24}px", "paddingRight": f"{RIGHT_PANEL_WIDTH + 24}px"}, children=[]),

        # Right tick panel
        html.Div(
            id="right-edge-control",
            role="region",
            **{"aria-label": "Tick control panel"},
            style={
                "position": "fixed",
                "top": "24px",
                "right": "0px",
                "width": f"{RIGHT_PANEL_WIDTH}px",
                "zIndex": 99999,
                "background": "linear-gradient(180deg, rgba(34,34,34,0.98), rgba(28,28,28,0.98))",
                "padding": "12px",
                "borderTopLeftRadius": "10px",
                "borderBottomLeftRadius": "10px",
                "borderLeft": "1px solid rgba(255,255,255,0.04)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.6)",
                "overflowY": "auto",
                "maxHeight": "92vh",
            },
            children=[
                html.Div("Tick", style={"fontSize": "14px", "color": "#ddd", "marginBottom": "8px", "textAlign": "center"}),
                dcc.Graph(id="tick-circle", figure=make_full_circle_figure(None), style={"height": f"{CARD_GRAPH_HEIGHT}px", "width": f"{RIGHT_PANEL_WIDTH}px"}),
                html.Div(
                    style={"marginTop": "8px", "display": "flex", "flexDirection": "column", "gap": "8px"},
                    children=[
                        dcc.Input(id="tick_input", type="text", placeholder="-2000..2000", style={
                            "width": "100%", "marginTop": "8px", "backgroundColor": "#1f1f1f", "color": "white",
                            "border": "1px solid #444", "padding": "8px", "borderRadius": "6px", "fontSize": "14px", "textAlign": "center", "boxSizing": "border-box"
                        }),
                        html.Div(style={"display": "flex", "gap": "8px"}, children=[
                            html.Button("Save", id="tick_save", n_clicks=0, style={"flex": "1", "backgroundColor": "#2b2b2b", "color": "white", "border": "1px solid #444", "padding": "8px", "borderRadius": "6px"}),
                            html.Button("Reset", id="tick_reset", n_clicks=0, style={"flex": "1", "backgroundColor": "#2b2b2b", "color": "white", "border": "1px solid #444", "padding": "8px", "borderRadius": "6px"}),
                        ]),
                        html.Div(id="tick-status", style={"marginTop": "6px", "color": "#bbb", "fontSize": "13px", "textAlign": "center"}),
                    ],
                ),
            ],
        ),
    ],
)

# -------------------------
# Tick callbacks (single writer for op-state)
# -------------------------
@app.callback(
    Output("op-state", "data"),
    Output("tick-status", "children"),
    Input("tick_save", "n_clicks"),
    Input("tick_reset", "n_clicks"),
    Input("tick_input", "n_submit"),
    State("tick_input", "value"),
    State("op-state", "data"),
    prevent_initial_call=True,
)
def write_state(tick_save, tick_reset, tick_submit, tick_value, current_state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    state = dict(current_state or {"tick": None, "history": []})
    if trigger == "tick_reset":
        state["tick"] = None
        state["history"] = (state.get("history") or []) + [{"ts": datetime.utcnow().isoformat(), "action": "reset"}]
        return state, "Tick reset."
    if trigger in ("tick_save", "tick_input"):
        if tick_value is None or str(tick_value).strip() == "":
            return no_update, "Enter a whole number before saving."
        s = str(tick_value).strip()
        if s.lstrip("+-").isdigit():
            val = int(s)
            if -MAX_RANGE <= val <= MAX_RANGE:
                state["tick"] = val
                state["history"] = (state.get("history") or []) + [{"ts": datetime.utcnow().isoformat(), "action": "save", "val": val}]
                return state, f"Saved: {val}"
            return no_update, f"Value must be between {-MAX_RANGE} and {MAX_RANGE}."
        return no_update, "Please enter a whole integer."
    return no_update, no_update

@app.callback(
    Output("tick-circle", "figure"),
    Input("op-state", "data"),
)
def update_tick_visual(op_state):
    saved_tick = None if op_state is None else op_state.get("tick")
    return make_full_circle_figure(saved_tick)

# -------------------------
# Single context-store writer (handles all buttons)
# -------------------------
@app.callback(
    Output("context-store", "data"),
    # Overnight buttons
    Input("overnight-btn-bullish", "n_clicks"),
    Input("overnight-btn-bullish_neutral", "n_clicks"),
    Input("overnight-btn-neutral", "n_clicks"),
    Input("overnight-btn-neutral_bearish", "n_clicks"),
    Input("overnight-btn-bearish", "n_clicks"),
    # Bigger buttons
    Input("bigger-btn-bullish", "n_clicks"),
    Input("bigger-btn-bullish_neutral", "n_clicks"),
    Input("bigger-btn-neutral", "n_clicks"),
    Input("bigger-btn-neutral_bearish", "n_clicks"),
    Input("bigger-btn-bearish", "n_clicks"),
    # Intermediate buttons
    Input("intermediate-btn-bullish", "n_clicks"),
    Input("intermediate-btn-bullish_neutral", "n_clicks"),
    Input("intermediate-btn-neutral", "n_clicks"),
    Input("intermediate-btn-neutral_bearish", "n_clicks"),
    Input("intermediate-btn-bearish", "n_clicks"),
    # Shortterm buttons
    Input("shortterm-btn-bullish", "n_clicks"),
    Input("shortterm-btn-bullish_neutral", "n_clicks"),
    Input("shortterm-btn-neutral", "n_clicks"),
    Input("shortterm-btn-neutral_bearish", "n_clicks"),
    Input("shortterm-btn-bearish", "n_clicks"),
    State("context-store", "data"),
    prevent_initial_call=True,
)
def update_context_store(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    parts = trigger_id.split("-btn-")
    if len(parts) != 2:
        return no_update
    card_prefix, sentiment = parts[0], parts[1]
    state = dict(args[-1] or {"overnight": None, "bigger_picture": None, "intermediate": None, "shortterm": None})
    if card_prefix == "overnight":
        state["overnight"] = sentiment
    elif card_prefix == "bigger":
        state["bigger_picture"] = sentiment
    elif card_prefix == "intermediate":
        state["intermediate"] = sentiment
    elif card_prefix == "shortterm":
        state["shortterm"] = sentiment
    return state

# -------------------------
# Style callbacks (read-only, update button styles)
# -------------------------
@app.callback(
    Output("overnight-btn-bullish", "style"),
    Output("overnight-btn-bullish_neutral", "style"),
    Output("overnight-btn-neutral", "style"),
    Output("overnight-btn-neutral_bearish", "style"),
    Output("overnight-btn-bearish", "style"),
    Input("context-store", "data"),
)
def style_overnight(context):
    selected = context.get("overnight") if context else None
    styles = []
    for val, _ in SENTIMENTS:
        s = dict(BUTTON_BASE_STYLE)
        if selected == val:
            col = BUTTON_COLORS[val]
            s["background"] = col["bg"]
            s["border"] = f"2px solid {col['border']}"
            s["color"] = col["text"]
        styles.append(s)
    return styles

@app.callback(
    Output("bigger-btn-bullish", "style"),
    Output("bigger-btn-bullish_neutral", "style"),
    Output("bigger-btn-neutral", "style"),
    Output("bigger-btn-neutral_bearish", "style"),
    Output("bigger-btn-bearish", "style"),
    Input("context-store", "data"),
)
def style_bigger(context):
    selected = context.get("bigger_picture") if context else None
    styles = []
    for val, _ in SENTIMENTS:
        s = dict(BUTTON_BASE_STYLE)
        if selected == val:
            col = BUTTON_COLORS[val]
            s["background"] = col["bg"]
            s["border"] = f"2px solid {col['border']}"
            s["color"] = col["text"]
        styles.append(s)
    return styles

@app.callback(
    Output("intermediate-btn-bullish", "style"),
    Output("intermediate-btn-bullish_neutral", "style"),
    Output("intermediate-btn-neutral", "style"),
    Output("intermediate-btn-neutral_bearish", "style"),
    Output("intermediate-btn-bearish", "style"),
    Input("context-store", "data"),
)
def style_intermediate(context):
    selected = context.get("intermediate") if context else None
    styles = []
    for val, _ in SENTIMENTS:
        s = dict(BUTTON_BASE_STYLE)
        if selected == val:
            col = BUTTON_COLORS[val]
            s["background"] = col["bg"]
            s["border"] = f"2px solid {col['border']}"
            s["color"] = col["text"]
        styles.append(s)
    return styles

@app.callback(
    Output("shortterm-btn-bullish", "style"),
    Output("shortterm-btn-bullish_neutral", "style"),
    Output("shortterm-btn-neutral", "style"),
    Output("shortterm-btn-neutral_bearish", "style"),
    Output("shortterm-btn-bearish", "style"),
    Input("context-store", "data"),
)
def style_shortterm(context):
    selected = context.get("shortterm") if context else None
    styles = []
    for val, _ in SENTIMENTS:
        s = dict(BUTTON_BASE_STYLE)
        if selected == val:
            col = BUTTON_COLORS[val]
            s["background"] = col["bg"]
            s["border"] = f"2px solid {col['border']}"
            s["color"] = col["text"]
        styles.append(s)
    return styles

# -------------------------
# Safety assertion: ensure exactly one writer for context-store
# -------------------------
def assert_single_store_writers(app, store_id="context-store"):
    found = []
    for cb_id, cb in app.callback_map.items():
        outputs = cb.get("outputs", [])
        for out in outputs:
            if isinstance(out, dict) and out.get("id") == store_id and out.get("property") == "data":
                found.append(cb_id)
    if len(found) > 1:
        raise RuntimeError(f"Multiple callbacks write {store_id}.data: {found}")

# Call the assertion after all callbacks are defined
assert_single_store_writers(app, "context-store")

if __name__ == "__main__":
    # disable the reloader to avoid duplicate callback registration while debugging
    app.run(debug=False)