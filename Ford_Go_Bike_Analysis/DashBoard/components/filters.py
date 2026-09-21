from dash import dcc

from components.colors import COLORS


def build_dropdown(
    component_id,
    options,
    default_all=True
):
    return dcc.Dropdown(
        id=component_id,
        className="custom-dropdown",
        options=[
            {
                "label": opt,
                "value": opt
            }
            for opt in options
        ],
        value=options if default_all else [],
        multi=True,
        placeholder="Select...",
        style={
            "marginBottom": "18px",
            "--Dash-Fill-Interactive-Strong": COLORS["primary"],
            "--Dash-Text-Primary": COLORS["text"],
            "--Dash-Stroke-Strong": COLORS.get("border", "#d7dce1"),
        },
    )