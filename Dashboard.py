from dash import dcc

from components.colors import COLORS


def build_dropdown(
    component_id,
    options,
    default_all=True
):
    return dcc.Dropdown(
        id=component_id,
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
        className="custom-dropdown",
        style={
            "marginBottom": "18px",
            "color": COLORS["text"],
            "fontFamily": "Arial, sans-serif",
            "fontSize": "13px",
        },
    )