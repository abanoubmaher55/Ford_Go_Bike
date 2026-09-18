import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output



df = pd.read_csv("Ford_Go_Bike\Ford_Go_Bike_Analysis\Part1-DataBase (Omar)\cleaned_data.csv")
df_time = pd.read_csv("Ford_Go_Bike\Ford_Go_Bike_Analysis\Part1-DataBase (Omar)\dim_time.csv")

df["start_time"] = pd.to_datetime(df["start_time"])

num_col = df.select_dtypes(include="number").columns

app = Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .Select-control, .Select-menu-outer, .Select-menu, .Select-value, .Select-placeholder {
                background-color: #121C15 !important;
                color: #E8F5E9 !important;
                border-color: #2C4432 !important;
            }
            .Select--multi .Select-value {
                background-color: #1B2A1F !important;
                border-color: #4CAF50 !important;
                color: #E8F5E9 !important;
            }
            .Select-input > input {
                color: #E8F5E9 !important;
            }
            .Select-arrow {
                border-color: #A5B5A7 transparent transparent !important;
            }
            .VirtualizedSelectOption {
                background-color: #121C15 !important;
                color: #E8F5E9 !important;
            }
            .VirtualizedSelectFocusedOption {
                background-color: #243528 !important;
                color: #E8F5E9 !important;
            }
            ::-webkit-scrollbar {
                width: 10px;
            }
            ::-webkit-scrollbar-track {
                background: #0B120D;
            }
            ::-webkit-scrollbar-thumb {
                background: #2C4432;
                border-radius: 10px;
            }
            body {
                background-color: #0B120D;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

COLORS = {
    "background": "#0B120D",
    "card": "#121C15",
    "card_hover": "#18251B",
    "primary": "#4CAF50",
    "secondary": "#66BB6A",
    "accent": "#81C784",
    "dark": "#071009",
    "light": "#1B2A1F",
    "very_light": "#243528",
    "text": "#E8F5E9",
    "muted_text": "#A5B5A7",
    "white": "#FFFFFF",
    "border": "#2C4432",
}

GREEN_THEME = {
    "dark": "#071009",
    "primary": "#4CAF50",
    "secondary": "#66BB6A",
    "light": "#81C784",
    "very_light": "#1B2A1F",
}

FONT_FAMILY = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"

USER_TYPE_OPTIONS = sorted(df["user_type"].dropna().unique().tolist())
GENDER_OPTIONS = sorted(df["member_gender"].dropna().unique().tolist())
AGE_GROUP_OPTIONS = sorted(df["age_group"].unique().tolist())
DAYS = sorted(df_time["day_of_week"].unique().tolist())



def build_checklist(component_id, options, default_all=True):
    """Small helper to keep checklist creation consistent + DRY."""
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": f" {opt}", "value": opt} for opt in options],
        value=options if default_all else [],
        multi=True,
        style={"marginBottom": "16px"},
    )


CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0, 0, 0, 0.4)",
    "padding": "18px 20px",
    "marginBottom": "18px",
    "border": f"1px solid {COLORS['border']}",
}


def side_bar():
    return html.Div(
        [
            html.H3("Filters", style={"color": COLORS["text"], "marginBottom": "18px"}),

            html.Label("User Type", style={"fontWeight": "600", "color": COLORS["accent"]}),
            build_checklist("user-type-filter", USER_TYPE_OPTIONS),

            html.Label("Gender", style={"fontWeight": "600", "color": COLORS["accent"]}),
            build_checklist("gender-filter", GENDER_OPTIONS),

            html.Label("Age Group", style={"fontWeight": "600", "color": COLORS["accent"]}),
            build_checklist("age-group-filter", AGE_GROUP_OPTIONS),

            html.Label("Day of Week", style={"fontWeight": "600", "color": COLORS["accent"]}),
            build_checklist("day-filter", DAYS),
        ],
        style={
            **CARD_STYLE,
            "width": "260px",
            "minWidth": "260px",
            "height": "fit-content",
            "position": "sticky",
            "top": "20px",
        },
    )


def build_header():
    return html.Div(
        [

            html.Div(
                [
                    html.Span(
                        "DATA ANALYTICS DASHBOARD",
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.08)",
                            "color": COLORS["accent"],
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "letterSpacing": "1.5px",
                            "padding": "5px 12px",
                            "borderRadius": "20px",
                            "display": "inline-block",
                            "marginBottom": "14px",
                            "border": f"1px solid rgba(255, 255, 255, 0.12)",
                        },
                    ),
                    html.H1(
                        [
                            html.Span("", style={"fontSize": "0.75em", "verticalAlign": "middle"}),
                            "Ford GoBike Analytics",
                        ],
                        style={
                            "color": COLORS["text"],
                            "fontFamily": "'Inter', 'Segoe UI', sans-serif",
                            "fontSize": "clamp(26px, 3.2vw, 36px)",
                            "fontWeight": "700",
                            "margin": "0 0 8px 0",
                            "letterSpacing": "-0.5px",
                        },
                    ),
                    html.P(
                        "Explore trip behavior, rider demographics, and mobility patterns.",
                        style={
                            "color": COLORS["muted_text"],
                            "fontFamily": "'Inter', 'Segoe UI', sans-serif",
                            "fontSize": "14.5px",
                            "fontWeight": "400",
                            "margin": "0",
                            "maxWidth": "480px",
                        },
                    ),
                ],
                style={"flex": "1 1 auto", "minWidth": "260px"},
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                "📅 ",
                                style={"fontSize": "13px", "marginRight": "6px"},
                            ),
                            html.Span(
                                "2019 Trip Analysis",
                                style={
                                    "color": COLORS["text"],
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.06)",
                            "border": "1px solid rgba(255, 255, 255, 0.10)",
                            "borderRadius": "10px",
                            "padding": "8px 14px",
                            "marginBottom": "10px",
                            "whiteSpace": "nowrap",
                        },
                    ),
                    html.Div(
                        [
                            html.Span(
                                "⚡ ",
                                style={"fontSize": "13px", "marginRight": "6px"},
                            ),
                            html.Span(
                                "Interactive Dashboard",
                                style={
                                    "color": COLORS["text"],
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.06)",
                            "border": "1px solid rgba(255, 255, 255, 0.10)",
                            "borderRadius": "10px",
                            "padding": "8px 14px",
                            "whiteSpace": "nowrap",
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
            "background": f"linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['light']} 55%, {COLORS['primary']} 100%)",
            "borderRadius": "18px",
            "boxShadow": "0 8px 24px rgba(0, 0, 0, 0.5)",
            "padding": "32px 40px",
            "marginBottom": "24px",
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "space-between",
            "alignItems": "center",
            "gap": "24px",
            "width": "100%",
            "boxSizing": "border-box",
            "border": f"1px solid {COLORS['border']}",
        },
    )

def graph_card(graph_id):
    """Wraps a single dcc.Graph in a white, rounded, shadowed card."""
    return html.Div(
        dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"height": "100%"}),
        style={
            "backgroundColor": COLORS["card"],
            "borderRadius": "16px",
            "boxShadow": "0 4px 16px rgba(0, 0, 0, 0.4)",
            "padding": "16px",
            "minWidth": "0",
            "border": f"1px solid {COLORS['border']}",
        },
    )


app.layout = html.Div([
    build_header(),
    html.Div(
        [
            side_bar(),
            html.Div(
                [
                    graph_card("gr1"),
                    graph_card("gr2"),
                    graph_card("gr3"),
                    graph_card("gr4"),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "20px",
                    "flex": "1 1 auto",
                    "minWidth": "0",
                },
            ),
        ],
        style={
            "backgroundColor": COLORS["background"],
            "minHeight": "100vh",
            "padding": "30px",
            "display": "flex",
            "gap": "20px",
            "alignItems": "flex-start",
        },
    )
], style={"backgroundColor": COLORS["background"]})
def style_figure(fig, x_title=None, y_title=None):
    """Applies consistent, modern styling to a Plotly figure in-place and returns it."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(family=FONT_FAMILY, size=13, color=COLORS["text"]),
        title=dict(
            font=dict(family=FONT_FAMILY, size=17, color=COLORS["accent"], weight="bold"),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=50, r=30, t=60, b=50),
        bargap=0.15,
        hoverlabel=dict(
            bgcolor=COLORS["light"],
            font=dict(family=FONT_FAMILY, size=12, color=COLORS["text"]),
            bordercolor=GREEN_THEME["secondary"],
        ),
        showlegend=False,
        height=360,
        autosize=True,
    )

    fig.update_xaxes(
        title=dict(text=x_title, font=dict(size=13, color=COLORS["muted_text"])),
        showgrid=False,
        showline=True,
        linecolor=COLORS["border"],
        tickfont=dict(size=11, color=COLORS["muted_text"]),
        zeroline=False,
    )

    fig.update_yaxes(
        title=dict(text=y_title, font=dict(size=13, color=COLORS["muted_text"])),
        showgrid=True,
        gridcolor=COLORS["border"],
        gridwidth=1,
        showline=False,
        tickfont=dict(size=11, color=COLORS["muted_text"]),
        zeroline=False,
    )

    return fig



def filter_dataframe(user_types, genders, age_groups, days):
    data = df.copy()
    if not user_types or not genders or not age_groups or not days:
        return data.iloc[0:0]

    if user_types:
        data = data[data["user_type"].isin(user_types)]

    if genders:
        data = data[data["member_gender"].isin(genders)]

    if age_groups:
        data = data[data["age_group"].isin(age_groups)]

    if days:
        data = data[data["day_of_week"].isin(days)]

    return data


@app.callback(
    Output("gr1", "figure"),
    Output("gr2", "figure"),
    Output("gr3", "figure"),
    Output("gr4", "figure"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("day-filter", "value"),
)
def update_dashboard(user_types, genders, age_groups, days):

    filtered = filter_dataframe(
        user_types,
        genders,
        age_groups,
        days
    )

    gender_counts = filtered["member_gender"].value_counts().reset_index()
    # Graph 1
    fig1 = px.histogram(
        filtered,
        x="duration_sec",
        nbins=30,
        title="Trip Duration Distribution",
        color_discrete_sequence=[GREEN_THEME["primary"]],
    )
    fig1.update_traces(marker_line_color=COLORS["dark"], marker_line_width=0.5, opacity=0.9)
    fig1 = style_figure(fig1, x_title="Duration (seconds)", y_title="Number of Trips")

    # Graph 2
    fig2 = px.histogram(
        filtered,
        x="users' age",
        nbins=30,
        title="Age Distribution",
        color_discrete_sequence=[GREEN_THEME["secondary"]],
    )
    fig2.update_traces(marker_line_color=COLORS["dark"], marker_line_width=0.5, opacity=0.9)
    fig2 = style_figure(fig2, x_title="Age", y_title="Number of Users")

    # Graph 3
    user_counts = filtered["user_type"].value_counts().reset_index()
    user_counts.columns = ["user_type", "count"]
    fig3 = px.bar(
        user_counts,
        x="user_type",
        y="count",
        title="Users by Type",
        color="user_type",
        color_discrete_sequence=[GREEN_THEME["light"], GREEN_THEME["primary"]],
    )
    fig3.update_traces(marker_line_width=0)
    fig3 = style_figure(fig3, x_title="User Type", y_title="Number of Users")

    # Graph 4
    gender_counts = filtered["member_gender"].value_counts().reset_index()
    gender_counts.columns = ["member_gender", "count"]
    fig4 = px.bar(
        gender_counts,
        x="member_gender",
        y="count",
        title="Users by Gender",
        color="member_gender",
        color_discrete_sequence=[GREEN_THEME["light"], GREEN_THEME["primary"], GREEN_THEME["secondary"]],
    )
    fig4.update_traces(marker_line_width=0)
    fig4 = style_figure(fig4, x_title="Gender", y_title="Number of Users")
    return fig1, fig2, fig3, fig4


if __name__ == "__main__":
    app.run(debug=True, port=3000)