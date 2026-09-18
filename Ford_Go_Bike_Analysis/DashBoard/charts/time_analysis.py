import plotly.express as px

from components.cards import style_figure
from components.colors import GREEN_THEME


def create_time_charts(filtered):

    # =====================================================
    # Graph 5 - Trips by Day
    # =====================================================

    DAYS = sorted(
        filtered["day_of_week"]
        .dropna()
        .unique()
        .tolist()
    )

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

    fig5.update_traces(
        marker_line_width=0,
        marker_color=GREEN_THEME["primary"],
    )

    fig5 = style_figure(
        fig5,

        x_title="Day",

        y_title="Number of Trips"
    )


    # =====================================================
    # Graph 6 - Trips by Hour
    # =====================================================

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

        color_discrete_sequence=[
            GREEN_THEME["secondary"]
        ],
    )

    fig6.update_traces(
        line=dict(
            width=3,
            color=GREEN_THEME["secondary"]
        ),

        marker=dict(
            size=7,
            color=GREEN_THEME["primary"]
        )
    )

    fig6 = style_figure(
        fig6,

        x_title="Hour of Day",

        y_title="Number of Trips"
    )


    # =====================================================
    # Return
    # =====================================================

    return (
        fig5,
        fig6
    )