from dash import html, dcc
from components.colors import (
    COLORS,
    GREEN_THEME,
    FONT_FAMILY
)

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
            "backgroundColor": COLORS["card"],
            "borderRadius": "16px",
            "border": (
                f"1px solid {COLORS['border']}"
            ),
            "boxShadow": (
                "0 4px 18px "
                "rgba(13, 92, 99, 0.12)"
            ),
            "padding": "16px",
            "minWidth": "0",
            "boxSizing": "border-box",
        },
    )

def style_figure(
    fig,
    x_title=None,
    y_title=None
):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(
            family=FONT_FAMILY,
            size=13,
            color=COLORS["text"]
        ),
        title=dict(
            font=dict(
                family=FONT_FAMILY,
                size=17,
                color=COLORS["dark"],
            ),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(
            l=50,
            r=30,
            t=60,
            b=50
        ),
        bargap=0.15,
        hoverlabel=dict(
            bgcolor=COLORS["dark"],
            font=dict(
                family=FONT_FAMILY,
                size=12,
                color=COLORS["white"]
            ),
            bordercolor=COLORS["primary"],
        ),
        showlegend=False,
        height=360,
        autosize=True,
    )

    fig.update_xaxes(
        title=dict(
            text=x_title,
            font=dict(
                size=13,
                color=COLORS["secondary_text"]
            )
        ),
        showgrid=False,
        showline=True,
        linecolor=COLORS["border"],
        tickfont=dict(
            size=11,
            color=COLORS["secondary_text"]
        ),
        zeroline=False,
    )

    fig.update_yaxes(
        title=dict(
            text=y_title,
            font=dict(
                size=13,
                color=COLORS["secondary_text"]
            )
        ),
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