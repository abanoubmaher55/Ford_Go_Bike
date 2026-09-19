from dash import html
from components.colors import COLORS
from components.sidebar import CARD_STYLE

def kpi_card(title, value_id):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "13px", "color": COLORS["text"], "opacity": 0.75}),
            html.Div(id=value_id, style={"fontSize": "26px", "fontWeight": "700", "color": COLORS["dark"]}),
        ],
        style={**CARD_STYLE, "flex": "1", "textAlign": "center", "minWidth": "180px"},
    )

def kpi_row():
    return html.Div(
        [
            kpi_card("Total Trips", "kpi-total-trips"),
            kpi_card("Average Trip Duration (min)", "kpi-avg-duration"),
            kpi_card("Unique Bikes", "kpi-unique-bikes")
        ],
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginTop": "6px", "marginBottom": "0px"},
    )