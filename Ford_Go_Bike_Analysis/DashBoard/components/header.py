from dash import html
from components.colors import (
    COLORS,
    FONT_FAMILY
)

def build_header():
    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        "DATA ANALYTICS DASHBOARD",
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.12)",
                            "color": "#FFFFFF",
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "letterSpacing": "1.5px",
                            "padding": "5px 12px",
                            "borderRadius": "20px",
                            "display": "inline-block",
                            "marginBottom": "14px",
                            "border": "1px solid rgba(255, 255, 255, 0.25)",
                        },
                    ),
                    html.H1(
                        "Ford GoBike Analytics",
                        style={
                            "color": "#FFFFFF",
                            "fontFamily": FONT_FAMILY,
                            "fontSize": "36px",
                            "fontWeight": "700",
                            "margin": "0 0 8px 0",
                            "letterSpacing": "-0.5px",
                        },
                    ),
                    html.P(
                        "Explore trip behavior, rider demographics, and mobility patterns.",
                        style={
                            "color": "#E0F4F1",
                            "fontFamily": FONT_FAMILY,
                            "fontSize": "14.5px",
                            "margin": "0",
                            "maxWidth": "480px",
                        },
                    ),
                ],
                style={
                    "flex": "1 1 auto",
                    "minWidth": "260px",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                "📅",
                                style={
                                    "fontSize": "13px",
                                    "marginRight": "6px",
                                },
                            ),
                            html.Span(
                                "2019 Trip Analysis",
                                style={
                                    "color": "#FFFFFF",
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.10)",
                            "border": "1px solid rgba(255, 255, 255, 0.20)",
                            "borderRadius": "10px",
                            "padding": "8px 14px",
                            "marginBottom": "10px",
                            "whiteSpace": "nowrap",
                            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.12)",
                        },
                    ),
                    html.Div(
                        [
                            html.Span(
                                "⚡",
                                style={
                                    "fontSize": "13px",
                                    "marginRight": "6px",
                                    "color": "#FFFFFF",
                                },
                            ),
                            html.Span(
                                "Interactive Dashboard",
                                style={
                                    "color": "#FFFFFF",
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.10)",
                            "border": "1px solid rgba(255, 255, 255, 0.20)",
                            "borderRadius": "10px",
                            "padding": "8px 14px",
                            "whiteSpace": "nowrap",
                            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.12)",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "flex-end",
                    "flex": "0 0 auto",
                },
            ),
        ],
        style={
            "background": "linear-gradient(135deg, #0D5C63 0%, #1F9E89 100%)",
            "border": "1px solid rgba(255, 255, 255, 0.18)",
            "borderRadius": "18px",
            "boxShadow": "0 8px 24px rgba(13, 92, 99, 0.25)",
            "padding": "32px 40px",
            "marginBottom": "24px",
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "space-between",
            "alignItems": "center",
            "gap": "24px",
            "width": "100%",
            "boxSizing": "border-box",
        },
    )