
import pandas as pd
import plotly.express as px
 
from components.cards import style_figure
from components.colors import GREEN_THEME
 
 
def create_overview_charts(filtered):
    """
    Overview tab now shows only the big-picture visual:
    a trend line of trips over time. Duration / Age / User Type /
    Gender charts moved to Trip Analysis and User Analysis.
    """
    trend_data = filtered.copy()
    trend_data["start_time"] = pd.to_datetime(trend_data["start_time"])
    trend_data["date"] = trend_data["start_time"].dt.date
 
    daily_trips = (
        trend_data.groupby("date")
        .size()
        .reset_index(name="trip_count")
    )
 
    fig_trend = px.line(
        daily_trips,
        x="date",
        y="trip_count",
        title="Trips Over Time",
        color_discrete_sequence=[GREEN_THEME["primary"]],
        markers=True,
    )
 
    fig_trend.update_traces(
        line_width=2,
        marker_size=4,
    )
 
    fig_trend = style_figure(
        fig_trend,
        x_title="Date",
        y_title="Number of Trips",
    )
 
    return (fig_trend,)
 
 
