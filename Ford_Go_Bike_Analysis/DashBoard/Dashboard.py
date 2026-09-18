import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# =========================================================
# 1. Load Data
# =========================================================

df = pd.read_csv(
    r"Ford_Go_Bike_Analysis\Part1-DataBase (Omar)\cleaned_data.csv"
)

df["start_time"] = pd.to_datetime(df["start_time"])

# Create hour column if it does not already exist
if "start_hour" not in df.columns:
    df["start_hour"] = df["start_time"].dt.hour


num_col = df.select_dtypes(include="number").columns


# =========================================================
# 2. Dash App
# =========================================================

app = Dash(__name__)

app.title = "Ford GoBike Analytics"


# =========================================================
# 3. Colors
# =========================================================

COLORS = {
    "background": "#8ECAE6",
    "primary": "#146C7A",
    "secondary": "#2A9D8F",
    "accent": "#8ECAE6",
    "light": "#8ECAE6",
    "dark": "#0D3B4C",
    "text": "#263238",
    "white": "#FFFFFF",
}


GREEN_THEME = {
    "dark": "#0D3B4C",
    "primary": "#146C7A",
    "secondary": "#2A9D8F",
    "light": "#8ECAE6",
    "very_light": "#8ECAE6",
}


FONT_FAMILY = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"


# =========================================================
# 4. Filter Options
# =========================================================

USER_TYPE_OPTIONS = sorted(
    df["user_type"].dropna().unique().tolist()
)

GENDER_OPTIONS = sorted(
    df["member_gender"].dropna().unique().tolist()
)

AGE_GROUP_OPTIONS = sorted(
    df["age_group"].dropna().unique().tolist()
)

DAYS = sorted(
    df["day_of_week"].dropna().unique().tolist()
)


# =========================================================
# 5. Checklist
# =========================================================

def build_checklist(component_id, options, default_all=True):
    """
    Create a reusable checklist for dashboard filters.
    """

    return dcc.Checklist(
        id=component_id,
        options=[
            {"label": f" {opt}", "value": opt}
            for opt in options
        ],
        value=options if default_all else [],
        labelStyle={
            "display": "block",
            "marginBottom": "4px",
            "color": COLORS["text"]
        },
        style={
            "marginBottom": "16px"
        },
    )


# =========================================================
# 6. Card Style
# =========================================================

CARD_STYLE = {
    "backgroundColor": COLORS["white"],
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(27, 94, 32, 0.12)",
    "padding": "18px 20px",
    "marginBottom": "18px",
}


# =========================================================
# 7. Sidebar
# =========================================================

def side_bar():

    return html.Div(
        [

            html.H3(
                "Filters",
                style={
                    "color": COLORS["dark"],
                    "marginBottom": "18px"
                }
            ),

            html.Label(
                "User Type",
                style={
                    "fontWeight": "600",
                    "color": COLORS["dark"]
                }
            ),

            build_checklist(
                "user-type-filter",
                USER_TYPE_OPTIONS
            ),

            html.Label(
                "Gender",
                style={
                    "fontWeight": "600",
                    "color": COLORS["dark"]
                }
            ),

            build_checklist(
                "gender-filter",
                GENDER_OPTIONS
            ),

            html.Label(
                "Age Group",
                style={
                    "fontWeight": "600",
                    "color": COLORS["dark"]
                }
            ),

            build_checklist(
                "age-group-filter",
                AGE_GROUP_OPTIONS
            ),

            html.Label(
                "Day of Week",
                style={
                    "fontWeight": "600",
                    "color": COLORS["dark"]
                }
            ),

            build_checklist(
                "day-filter",
                DAYS
            ),

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


# =========================================================
# 8. Header
# =========================================================

def build_header():

    return html.Div(
        [

            html.Div(
                [

                    html.Span(
                        "DATA ANALYTICS DASHBOARD",
                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.12)",
                            "color": COLORS["light"],
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "letterSpacing": "1.5px",
                            "padding": "5px 12px",
                            "borderRadius": "20px",
                            "display": "inline-block",
                            "marginBottom": "14px",
                            "border": "1px solid rgba(255, 255, 255, 0.18)",
                        },
                    ),

                    html.H1(
                        "Ford GoBike Analytics",
                        style={
                            "color": COLORS["white"],
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
                            "color": "rgba(255, 255, 255, 0.75)",
                            "fontFamily": FONT_FAMILY,
                            "fontSize": "14.5px",
                            "margin": "0",
                            "maxWidth": "480px",
                        },
                    ),

                ],

                style={
                    "flex": "1 1 auto",
                    "minWidth": "260px"
                },
            ),

            html.Div(
                [

                    html.Div(
                        [
                            html.Span(
                                "📅 ",
                                style={
                                    "fontSize": "13px",
                                    "marginRight": "6px"
                                },
                            ),

                            html.Span(
                                "2019 Trip Analysis",
                                style={
                                    "color": COLORS["white"],
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],

                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.08)",
                            "border": "1px solid rgba(255, 255, 255, 0.14)",
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
                                style={
                                    "fontSize": "13px",
                                    "marginRight": "6px"
                                },
                            ),

                            html.Span(
                                "Interactive Dashboard",
                                style={
                                    "color": COLORS["white"],
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                },
                            ),
                        ],

                        style={
                            "backgroundColor": "rgba(255, 255, 255, 0.08)",
                            "border": "1px solid rgba(255, 255, 255, 0.14)",
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
            "background": f"linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['primary']} 55%, {COLORS['secondary']} 100%)",
            "borderRadius": "18px",
            "boxShadow": "0 8px 24px rgba(27, 94, 32, 0.28)",
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


# =========================================================
# 9. Graph Card
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
            "backgroundColor": COLORS["white"],
            "borderRadius": "16px",
            "boxShadow": "0 4px 16px rgba(27, 94, 32, 0.10)",
            "padding": "16px",
            "minWidth": "0",
        },
    )


# =========================================================
# 10. Figure Style
# =========================================================

def style_figure(fig, x_title=None, y_title=None):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font=dict(
            family=FONT_FAMILY,
            size=13,
            color="#37474F"
        ),

        title=dict(
            font=dict(
                family=FONT_FAMILY,
                size=17,
                color=GREEN_THEME["dark"],
                weight="bold"
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
            bgcolor="#FFFFFF",
            font=dict(
                family=FONT_FAMILY,
                size=12,
                color="#263238"
            ),
            bordercolor=GREEN_THEME["secondary"],
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
                color="#455A64"
            )
        ),
        showgrid=False,
        showline=True,
        linecolor="#CFD8DC",
        tickfont=dict(
            size=11,
            color="#607D8B"
        ),
        zeroline=False,
    )

    fig.update_yaxes(
        title=dict(
            text=y_title,
            font=dict(
                size=13,
                color="#455A64"
            )
        ),
        showgrid=True,
        gridcolor="#EEF3EC",
        gridwidth=1,
        showline=False,
        tickfont=dict(
            size=11,
            color="#607D8B"
        ),
        zeroline=False,
    )

    return fig


# =========================================================
# 11. Filter Data
# =========================================================

def filter_dataframe(
    user_types,
    genders,
    age_groups,
    days
):

    if (
        not user_types
        or not genders
        or not age_groups
        or not days
    ):
        return df.iloc[0:0]

    data = df.copy()

    data = data[
        data["user_type"].isin(user_types)
    ]

    data = data[
        data["member_gender"].isin(genders)
    ]

    data = data[
        data["age_group"].isin(age_groups)
    ]

    data = data[
        data["day_of_week"].isin(days)
    ]

    return data


# =========================================================
# 12. Tabs
# =========================================================

tabs = dcc.Tabs(

    id="tabs",

    value="overview",

    children=[

        # -------------------------------------------------
        # Overview
        # -------------------------------------------------

        dcc.Tab(

            label="Overview",

            value="overview",

            children=[

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
                        "paddingTop": "20px",
                    },
                )

            ],
        ),


        # -------------------------------------------------
        # Time Analysis
        # -------------------------------------------------

        dcc.Tab(

            label="Time Analysis",

            value="time",

            children=[

                html.Div(
                    [

                        graph_card("gr5"),
                        graph_card("gr6"),

                    ],

                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px",
                        "paddingTop": "20px",
                    },
                )

            ],
        ),


        # -------------------------------------------------
        # User Analysis
        # -------------------------------------------------

        dcc.Tab(

            label="User Analysis",

            value="user",

            children=[

                html.Div(
                    [

                        graph_card("gr7"),
                        graph_card("gr8"),
                        graph_card("gr9"),

                    ],

                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px",
                        "paddingTop": "20px",
                    },
                )

            ],
        ),


        # -------------------------------------------------
        # Trip Analysis
        # -------------------------------------------------

        dcc.Tab(

            label="Trip Analysis",

            value="trip",

            children=[

                html.Div(
                    [

                        graph_card("gr10"),
                        graph_card("gr11"),

                    ],

                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px",
                        "paddingTop": "20px",
                    },
                )

            ],
        ),

    ],

    style={
        "backgroundColor": COLORS["white"],
        "borderRadius": "12px",
    },
)


# =========================================================
# 13. Main Layout
# =========================================================

app.layout = html.Div(

    [

        build_header(),

        html.Div(

            [

                side_bar(),

                html.Div(
                    [
                        tabs
                    ],

                    style={
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
        ),

    ]
)


# =========================================================
# 14. Callback
# =========================================================

@app.callback(

    Output("gr1", "figure"),
    Output("gr2", "figure"),
    Output("gr3", "figure"),
    Output("gr4", "figure"),

    Output("gr5", "figure"),
    Output("gr6", "figure"),

    Output("gr7", "figure"),
    Output("gr8", "figure"),
    Output("gr9", "figure"),

    Output("gr10", "figure"),
    Output("gr11", "figure"),

    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("day-filter", "value"),
)


def update_dashboard(
    user_types,
    genders,
    age_groups,
    days
):

    # Filter data
    filtered = filter_dataframe(
        user_types,
        genders,
        age_groups,
        days
    )


    # =====================================================
    # OVERVIEW
    # =====================================================

    # Graph 1 - Trip Duration
    fig1 = px.histogram(
        filtered,
        x="duration_sec",
        nbins=30,
        title="Trip Duration Distribution",
        color_discrete_sequence=[
            GREEN_THEME["primary"]
        ],
    )

    fig1.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=0.5,
        opacity=0.9
    )

    fig1 = style_figure(
        fig1,
        x_title="Duration (seconds)",
        y_title="Number of Trips"
    )


    # Graph 2 - Age
    fig2 = px.histogram(
        filtered,
        x="users' age",
        nbins=30,
        title="Age Distribution",
        color_discrete_sequence=[
            GREEN_THEME["secondary"]
        ],
    )

    fig2.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=0.5,
        opacity=0.9
    )

    fig2 = style_figure(
        fig2,
        x_title="Age",
        y_title="Number of Users"
    )


    # Graph 3 - User Type
    user_counts = (
        filtered["user_type"]
        .value_counts()
        .reset_index()
    )

    user_counts.columns = [
        "user_type",
        "count"
    ]

    fig3 = px.bar(
        user_counts,
        x="user_type",
        y="count",
        title="Users by Type",
        color="user_type",
        color_discrete_sequence=[
            GREEN_THEME["dark"],
            GREEN_THEME["light"]
        ],
    )

    fig3.update_traces(
        marker_line_width=0
    )

    fig3 = style_figure(
        fig3,
        x_title="User Type",
        y_title="Number of Users"
    )


    # Graph 4 - Gender
    gender_counts = (
        filtered["member_gender"]
        .value_counts()
        .reset_index()
    )

    gender_counts.columns = [
        "member_gender",
        "count"
    ]

    fig4 = px.bar(
        gender_counts,
        x="member_gender",
        y="count",
        title="Users by Gender",
        color="member_gender",
        color_discrete_sequence=[
            GREEN_THEME["dark"],
            GREEN_THEME["primary"],
            GREEN_THEME["light"]
        ],
    )

    fig4.update_traces(
        marker_line_width=0
    )

    fig4 = style_figure(
        fig4,
        x_title="Gender",
        y_title="Number of Users"
    )


    # =====================================================
    # TIME ANALYSIS
    # =====================================================

    # Graph 5 - Trips by Day
    day_counts = (
        filtered["day_of_week"]
        .value_counts()
        .reindex(DAYS)
        .fillna(0)
        .reset_index()
    )

    day_counts.columns = [
        "day_of_week",
        "count"
    ]

    fig5 = px.bar(
        day_counts,
        x="day_of_week",
        y="count",
        title="Trips by Day of Week",
        color_discrete_sequence=[
            GREEN_THEME["primary"]
        ],
    )

    fig5 = style_figure(
        fig5,
        x_title="Day",
        y_title="Number of Trips"
    )


    # Graph 6 - Trips by Hour
    hour_counts = (
        filtered["start_hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    hour_counts.columns = [
        "start_hour",
        "count"
    ]

    fig6 = px.line(
        hour_counts,
        x="start_hour",
        y="count",
        markers=True,
        title="Trips by Hour",
    )

    fig6.update_traces(
        line_width=3
    )

    fig6 = style_figure(
        fig6,
        x_title="Hour of Day",
        y_title="Number of Trips"
    )


    # =====================================================
    # USER ANALYSIS
    # =====================================================

    # Graph 7 - User Type
    fig7 = px.pie(
        filtered,
        names="user_type",
        title="User Type Distribution",
        hole=0.45,
    )

    fig7.update_layout(
        showlegend=True
    )

    fig7 = style_figure(fig7)


    # Graph 8 - Gender
    fig8 = px.pie(
        filtered,
        names="member_gender",
        title="Gender Distribution",
        hole=0.45,
    )

    fig8.update_layout(
        showlegend=True
    )

    fig8 = style_figure(fig8)


    # Graph 9 - Age Groups
    age_counts = (
        filtered["age_group"]
        .value_counts()
        .reset_index()
    )

    age_counts.columns = [
        "age_group",
        "count"
    ]

    fig9 = px.bar(
        age_counts,
        x="age_group",
        y="count",
        title="Users by Age Group",
        color_discrete_sequence=[
            GREEN_THEME["secondary"]
        ],
    )

    fig9 = style_figure(
        fig9,
        x_title="Age Group",
        y_title="Number of Users"
    )


    # =====================================================
    # TRIP ANALYSIS
    # =====================================================

    # Graph 10 - Trip Duration
    fig10 = px.box(
        filtered,
        y="duration_sec",
        title="Trip Duration Box Plot",
        color_discrete_sequence=[
            GREEN_THEME["primary"]
        ],
    )

    fig10 = style_figure(
        fig10,
        y_title="Duration (seconds)"
    )


    # Graph 11 - Duration by User Type
    fig11 = px.box(
        filtered,
        x="user_type",
        y="duration_sec",
        title="Trip Duration by User Type",
        color="user_type",
        color_discrete_sequence=[
            GREEN_THEME["dark"],
            GREEN_THEME["secondary"]
        ],
    )

    fig11 = style_figure(
        fig11,
        x_title="User Type",
        y_title="Duration (seconds)"
    )


    return (
        fig1,
        fig2,
        fig3,
        fig4,
        fig5,
        fig6,
        fig7,
        fig8,
        fig9,
        fig10,
        fig11,
    )


# =========================================================
# 15. Run App
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=3000)