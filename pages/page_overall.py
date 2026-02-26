import dash_svg as svg
from dash import html, dcc
import dash_svg as svg
import math

def layout_overall(tick_value):

    # -------------------------------
    # NEEDLE ANGLE
    # -------------------------------
    angle = (tick_value / 1200) * 120
    rad = math.radians(angle - 90)

    cx, cy = 225, 225
    needle_length = 160
    x2 = cx + needle_length * math.cos(rad)
    y2 = cy + needle_length * math.sin(rad)

    # -------------------------------
    # ARC GEOMETRY
    # -------------------------------
    radius = 200
    start_angle = -120
    end_angle = 120

    def polar_to_cart(angle_deg):
        a = math.radians(angle_deg - 90)
        return (
            cx + radius * math.cos(a),
            cy + radius * math.sin(a)
        )

    x_start, y_start = polar_to_cart(start_angle)
    x_end, y_end = polar_to_cart(end_angle)

    large_arc_flag = 1

    arc_path = (
        f"M {x_start} {y_start} "
        f"A {radius} {radius} 0 {large_arc_flag} 1 {x_end} {y_end}"
    )

    # -------------------------------
    # TICK MARKS
    # -------------------------------
    tick_values = [-1000, -800, -600, 600, 800, 1000]
    tick_lines = []

    for tv in tick_values:
        t_angle = (tv / 1200) * 120
        rad1 = math.radians(t_angle - 90)

        outer_r = radius + 4
        inner_r = radius - 12

        x_outer = cx + outer_r * math.cos(rad1)
        y_outer = cy + outer_r * math.sin(rad1)
        x_inner = cx + inner_r * math.cos(rad1)
        y_inner = cy + inner_r * math.sin(rad1)

        tick_lines.append(
            svg.Line(
                x1=str(x_inner),
                y1=str(y_inner),
                x2=str(x_outer),
                y2=str(y_outer),
                stroke="#ffffff",
                strokeWidth="3"
            )
        )

    # -------------------------------
    # RAW SVG FILTER (Glow)
    # -------------------------------
    filter_defs = dcc.Markdown(
        """
        <svg width="0" height="0">
            <defs>
                <filter id="outerGlow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
        </svg>
        """,
        dangerously_allow_html=True
    )

    # -------------------------------
    # SVG LAYOUT USING dash_svg
    # -------------------------------
    gauge_svg = svg.Svg(
        width="450",
        height="450",
        viewBox="0 0 450 450",
        children=[
            # GRADIENT
            svg.Defs([
                svg.LinearGradient(
                    id="arcGradient",
                    gradientUnits="userSpaceOnUse",
                    x1="0", y1="0", x2="450", y2="0",
                    gradientTransform="rotate(120,225,225)",
                    children=[
                        svg.Stop(style={"stop-color": "#8B0000", "offset": "0%"}),
                        svg.Stop(style={"stop-color": "#B00000", "offset": "10%"}),
                        svg.Stop(style={"stop-color": "#CC0000", "offset": "20%"}),
                        svg.Stop(style={"stop-color": "#FF6666", "offset": "30%"}),
                        svg.Stop(style={"stop-color": "#EDE9D9", "offset": "45%"}),
                        svg.Stop(style={"stop-color": "#FAF7EF", "offset": "50%"}),  # warm white
                        svg.Stop(style={"stop-color": "#EDE9D9", "offset": "55%"}),
                        svg.Stop(style={"stop-color": "#66FF66", "offset": "70%"}),
                        svg.Stop(style={"stop-color": "#00CC00", "offset": "80%"}),
                        svg.Stop(style={"stop-color": "#009900", "offset": "90%"}),
                        svg.Stop(style={"stop-color": "#006600", "offset": "100%"}),
                    ]
                )
            ]),

            # ARC — NUCLEAR OVERRIDE (inline + attribute)
            svg.Path(
                id="arc-path",
                d=arc_path,
                stroke="url(#arcGradient)",  # attribute
                strokeWidth="16",
                strokeLinecap="round",
                fill="none",
                style={
                    "filter": "url(#outerGlow)",
                    "stroke": "url(#arcGradient)"  # inline override
                }
            ),

            # TICKS
            *tick_lines,

            # NEEDLE
            svg.Line(
                x1=str(cx),
                y1=str(cy),
                x2=str(x2),
                y2=str(y2),
                stroke="#ffffff",
                strokeWidth="6",
                strokeLinecap="round"
            ),

            # HUB
            svg.Circle(
                cx=str(cx),
                cy=str(cy),
                r="10",
                fill="#ffffff"
            )
        ]
    )

    # -------------------------------
    # RETURN LAYOUT
    # -------------------------------
    return html.Div(
        id="overall-content",
        children=[
            filter_defs,
            html.H2(
                "Overall Picture",
                style={"color": "#ffffff", "textAlign": "center"}
            ),
            html.Div(gauge_svg, style={"textAlign": "center"}),
            html.Div(
                f"Tick Value: {tick_value}",
                style={
                    "color": "#ffffff",
                    "marginTop": "20px",
                    "fontSize": "20px",
                    "textAlign": "center"
                }
            )
        ],
        style={"padding": "20px"}
    )
