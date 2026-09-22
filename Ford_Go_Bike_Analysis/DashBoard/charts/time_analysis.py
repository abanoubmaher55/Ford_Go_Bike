import pandas as pd
import plotly.express as px
 
from components.cards import style_figure
from components.colors import GREEN_THEME
 
# Fixed order: Monday -> Sunday
DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
 
 
def create_time_charts(filtered):
    # Only keep days that actually exist in the data, but always in Mon->Sun order
    DAYS = [d for d in DAY_ORDER if d in filtered["day_of_week"].dropna().unique()]
 
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
        category_orders={"day_of_week": DAYS},
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
 
    weekend_days = [d for d in ["Saturday", "Sunday"] if d in DAYS]
 
    fig13 = px.pie(
        filtered[filtered["day_of_week"].isin(weekend_days)]
        .value_counts("day_of_week")
        .reindex(weekend_days, fill_value=0)
        .reset_index(name="count"),
 
        names="day_of_week",
        hole=0.4,
        title="Number of Trips by Weekend Day",
        category_orders={"day_of_week": weekend_days},
 
        color_discrete_sequence=[
            GREEN_THEME["primary"]
        ],
    )
 
    fig13.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Number of Trips",
    )
 
    # ------------------------------------------------------------------
    # Weekday vs Weekend comparison (average trips per day)
    # ------------------------------------------------------------------
    weekday_days = [d for d in DAYS if d not in ["Saturday", "Sunday"]]
 
    group_avg = pd.DataFrame({
        "group": ["Weekday", "Weekend"],
        "avg_trips": [
            day_counts[day_counts["day_of_week"].isin(weekday_days)]["count"].mean()
            if weekday_days else 0,
            day_counts[day_counts["day_of_week"].isin(weekend_days)]["count"].mean()
            if weekend_days else 0,
        ],
    })
 
    fig15 = px.bar(
        group_avg,
        x="group",
        y="avg_trips",
        title="Weekday vs Weekend (Avg Trips per Day)",
        color="group",
        color_discrete_sequence=[
            GREEN_THEME["primary"],
            GREEN_THEME["secondary"],
        ],
    )
 
    fig15 = style_figure(
        fig15,
        x_title="",
        y_title="Average Number of Trips"
    )
 
    fig15.update_layout(showlegend=False)
 
    return (
        fig5,
        fig6,
        fig13,
        fig15,
    )
 
