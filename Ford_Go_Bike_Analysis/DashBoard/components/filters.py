from dash import dcc

from components.colors import COLORS


# =========================================================
# Checklist
# =========================================================

def build_checklist(
    component_id,
    options,
    default_all=True
):

    """
    Create a reusable checklist for dashboard filters.
    """

    return dcc.Checklist(

        id=component_id,

        # =====================================================
        # Options
        # =====================================================

        options=[
            {
                "label": f" {opt}",
                "value": opt
            }

            for opt in options
        ],

        value=options if default_all else [],

        # =====================================================
        # Text
        # =====================================================

        labelStyle={
            "display": "block",

            "marginBottom": "7px",

            "color": COLORS["text"],

            "fontSize": "13px",

            "fontFamily": "Arial, sans-serif",
        },

        # =====================================================
        # Checkbox
        # =====================================================

        inputStyle={
            "marginRight": "8px",

            # Teal instead of old green
            "accentColor": COLORS["primary"],
        },

        # =====================================================
        # Container
        # =====================================================

        style={
            "marginBottom": "18px",
        },
    )