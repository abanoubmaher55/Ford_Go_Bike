from dash import html, dcc

from components.colors import (
    COLORS,
    GREEN_THEME,
    FONT_FAMILY
)


# =========================================================
# Graph Card
# =========================================================

def graph_card(graph_id):

    return html.Div(

        dcc.Graph(
            id=graph_id,

            config={
                "displayModeBar": False
            },

            style={
                "height": "100%"
            },
        ),

        style={

            # =================================================
            # Card Background
            # =================================================

            "backgroundColor": COLORS["card"],

            "borderRadius": "16px",

            # =================================================
            # Border
            # =================================================

            "border": (
                f"1px solid {COLORS['border']}"
            ),

            # =================================================
            # Shadow
            # =================================================

            "boxShadow": (
                "0 4px 18px "
                "rgba(13, 92, 99, 0.12)"
            ),

            "padding": "16px",

            "minWidth": "0",

            "boxSizing": "border-box",
        },
    )


# =========================================================
# Figure Styling
# =========================================================

def style_figure(
    fig,
    x_title=None,
    y_title=None
):

    fig.update_layout(

        # =================================================
        # Light Plotly Theme
        # =================================================

        template="plotly_white",

        paper_bgcolor=COLORS["card"],

        plot_bgcolor=COLORS["card"],


        # =================================================
        # Font
        # =================================================

        font=dict(

            family=FONT_FAMILY,

            size=13,

            color=COLORS["text"]
        ),


        # =================================================
        # Title
        # =================================================

        title=dict(

            font=dict(

                family=FONT_FAMILY,

                size=17,

                color=COLORS["dark"],
            ),

            x=0.02,

            xanchor="left",
        ),


        # =================================================
        # Spacing
        # =================================================

        margin=dict(

            l=50,

            r=30,

            t=60,

            b=50
        ),

        bargap=0.15,


        # =================================================
        # Hover
        # =================================================

        hoverlabel=dict(

            bgcolor=COLORS["dark"],

            font=dict(

                family=FONT_FAMILY,

                size=12,

                color=COLORS["white"]
            ),

            bordercolor=COLORS["primary"],
        ),


        # =================================================
        # Legend
        # =================================================

        showlegend=False,


        # =================================================
        # Size
        # =================================================

        height=360,

        autosize=True,
    )


    # =====================================================
    # X Axis
    # =====================================================

    fig.update_xaxes(

        title=dict(

            text=x_title,

            font=dict(

                size=13,

                color=COLORS["secondary_text"]
            )
        ),

        # No vertical grid
        showgrid=False,

        showline=True,

        linecolor=COLORS["border"],

        tickfont=dict(

            size=11,

            color=COLORS["secondary_text"]
        ),

        zeroline=False,
    )


    # =====================================================
    # Y Axis
    # =====================================================

    fig.update_yaxes(

        title=dict(

            text=y_title,

            font=dict(

                size=13,

                color=COLORS["secondary_text"]
            )
        ),

        # Horizontal grid
        showgrid=True,

        gridcolor=COLORS["border"],

        gridwidth=1,

        showline=False,

        tickfont=dict(

            size=11,

            color=COLORS["secondary_text"]
        ),

        zeroline=False,
    )


    # =====================================================
    # General Colors
    # =====================================================

    fig.update_layout(

    colorway=[
        GREEN_THEME["primary"],
        GREEN_THEME["secondary"],
        GREEN_THEME["dark"],
        GREEN_THEME["light"],
        GREEN_THEME["accent"],
    ],

    selectionrevision="teal-theme",
    )


    return fig