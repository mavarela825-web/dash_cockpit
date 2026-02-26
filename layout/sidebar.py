from dash import html, dcc

def sidebar():
    return html.Div(
        [
            html.H2("Navigation", style={"color": "#ffffff", "textAlign": "center"}),

            dcc.Link("Overall Picture", href="/overall", className="sidebar-link"),
            dcc.Link("Context", href="/context", className="sidebar-link"),
            dcc.Link("Bias", href="/bias", className="sidebar-link"),
            dcc.Link("Tick", href="/tick", className="sidebar-link"),
            dcc.Link("AD Line", href="/adline", className="sidebar-link"),
        ],
        style={
            "width": "220px",
            "backgroundColor": "#111111",
            "padding": "20px",
            "height": "100vh",
            "position": "fixed",
            "left": "0",
            "top": "0",
            "overflowY": "auto",
        }
    )
