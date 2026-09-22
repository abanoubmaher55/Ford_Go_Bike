from dash import dcc, html
from components.cards import graph_card
from components.colors import COLORS , GREEN_THEME
from components.kpi import kpi_row
 
def build_tabs():
    return dcc.Tabs(
        id="tabs",
        value="overview",
        colors={
            "border": COLORS["border"],
            "primary": COLORS["tab_active"],
            "background": COLORS["card"],
        },
        children=[
            dcc.Tab(
                label="Overview",
                value="overview",
                children=[
                    kpi_row(),
                    html.Div(
                        [
                            graph_card("gr1"),
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr",
                            "gap": "20px",
                            "paddingTop": "20px",
                        },
                    )
                ],
                style={
                    "backgroundColor": COLORS["card"],
                    "color": COLORS["text"],
                    "border": "none",
                    "padding": "12px 20px",
                    "fontWeight": "600",
                },
                selected_style={
                    "backgroundColor": COLORS["card"],
                    "color": GREEN_THEME['primary'],
                    "borderTop": f"3px solid {GREEN_THEME['primary']}",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderBottom": "none",
                    "padding": "12px 20px",
                    "fontWeight": "700",
                },
            ),
            dcc.Tab(
                label="Time Analysis",
                value="time",
                children=[
                    html.Div(
                        [
                            graph_card("gr5"),
                            graph_card("gr6"),
                            graph_card("gr13"),
                            graph_card("gr15"),
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "20px",
                            "paddingTop": "20px",
                        },
                    )
                ],
                style={
                    "backgroundColor": COLORS["card"],
                    "color": COLORS["text"],
                    "border": "none",
                    "padding": "12px 20px",
                    "fontWeight": "600",
                },
                selected_style={
                    "backgroundColor": COLORS["card"],
                    "color": GREEN_THEME['primary'],
                    "borderTop": f"3px solid {GREEN_THEME['primary']}",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderBottom": "none",
                    "padding": "12px 20px",
                    "fontWeight": "700",
                },
            ),
            dcc.Tab(
                label="User Analysis",
                value="user",
                children=[
                    html.Div(
                        [
                            graph_card("gr7"),
                            graph_card("gr8"),
                            graph_card("gr9"),
                            graph_card("gr14"),
                            graph_card("gr17"),
                            graph_card("gr18"),
                            
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "20px",
                            "paddingTop": "20px",
                        },
                    )
                ],
                style={
                    "backgroundColor": COLORS["card"],
                    "color": COLORS["text"],
                    "border": "none",
                    "padding": "12px 20px",
                    "fontWeight": "600",
                },
                selected_style={
                    "backgroundColor": COLORS["card"],
                    "color": GREEN_THEME['primary'],
                    "borderTop": f"3px solid {GREEN_THEME['primary']}",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderBottom": "none",
                    "padding": "12px 20px",
                    "fontWeight": "700",
                },
            ),
            dcc.Tab(
                label="Trip Analysis",
                value="trip",
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Stations Map",
                                        style={
                                            "color": COLORS["primary"],
                                            "marginBottom": "5px",
                                            "fontSize": "20px",
                                            "fontWeight": "700",
                                        },
                                    ),
                                    html.P(
                                        "Departure hotspots by volume",
                                        style={
                                            "color": COLORS["muted_text"],
                                            "marginTop": "0px",
                                            "fontSize": "13px",
                                        },
                                    ),
                                    dcc.Graph(
                                        id="stations-map",
                                        config={
                                            "scrollZoom": True,
                                            "displayModeBar": True,
                                            "displaylogo": False,
                                        },
                                        style={
                                            "height": "500px",
                                        },
                                    ),
                                ],
                                style={
                                    "gridColumn": "1 / -1",
                                    "backgroundColor": COLORS["card"],
                                    "border": f"1px solid {COLORS['border']}",
                                    "borderRadius": "16px",
                                    "padding": "15px",
                                    "marginBottom": "0px",
                                    "boxShadow": "0 4px 20px rgba(13, 92, 99, 0.12)",
                                },
                            ),
                            graph_card("gr10"),
                            graph_card("gr11"),
                            graph_card("gr12"),
                            graph_card("route-flow-map"),
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "20px",
                            "paddingTop": "20px",
                        },
                    )
                ],
                style={
                    "backgroundColor": COLORS["card"],
                    "color": COLORS["text"],
                    "border": "none",
                    "padding": "12px 20px",
                    "fontWeight": "600",
                },
                selected_style={
                    "backgroundColor": COLORS["card"],
                    "color": GREEN_THEME['primary'],
                    "borderTop": f"3px solid {GREEN_THEME['primary']}",
                    "borderLeft": "none",
                    "borderRight": "none",
                    "borderBottom": "none",
                    "padding": "12px 20px",
                    "fontWeight": "700",
                },
            ),
        ],
        style={
            "backgroundColor": COLORS["card"],
            "borderRadius": "12px",
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['border']}",
            "overflow": "hidden",
        },
    )
 
