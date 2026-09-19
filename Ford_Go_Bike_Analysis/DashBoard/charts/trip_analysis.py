import plotly.express as px
import plotly.graph_objects as go

from components.cards import style_figure
from components.colors import COLORS, GREEN_THEME

def create_trip_charts(filtered):
    departures = (
        filtered
        .groupby("start_station_name")
        .size()
        .reset_index(name="Departures")
        .rename(
            columns={
                "start_station_name": "station"
            }
        )
    )

    arrivals = (
        filtered
        .groupby("end_station_name")
        .size()
        .reset_index(name="Arrivals")
        .rename(
            columns={
                "end_station_name": "station"
            }
        )
    )

    station_flow = departures.merge(
        arrivals,
        on="station",
        how="outer"
    ).fillna(0)

    station_flow["total"] = (
        station_flow["Departures"]
        + station_flow["Arrivals"]
    )

    station_flow = station_flow.sort_values(
        "total",
        ascending=True
    )

    fig_station = go.Figure()

    fig_station.add_trace(
        go.Bar(
            y=station_flow["station"],
            x=-station_flow["Departures"],
            orientation="h",
            name="Departures",
            marker_color=GREEN_THEME["dark"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Departures: %{customdata}<extra></extra>"
            ),
            customdata=station_flow["Departures"],
        )
    )

    fig_station.add_trace(
        go.Bar(
            y=station_flow["station"],
            x=station_flow["Arrivals"],
            orientation="h",
            name="Arrivals",
            marker_color=GREEN_THEME["primary"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Arrivals: %{x}<extra></extra>"
            ),
        )
    )

    fig_station.update_layout(
        title="Station Flow",
        barmode="relative",
        xaxis_title="Trips",
        yaxis_title="Station",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    fig_station = style_figure(
        fig_station,
        x_title="Trips",
        y_title="Station",
    )

    fig_station.update_layout(
        showlegend=True
    )

    route_data = filtered.copy()

    route_data["start_station_name"] = (
        route_data["start_station_name"]
        .fillna("Unknown")
        .astype(str)
    )

    route_data["end_station_name"] = (
        route_data["end_station_name"]
        .fillna("Unknown")
        .astype(str)
    )

    route_data["route"] = (
        route_data["start_station_name"]
        + " → "
        + route_data["end_station_name"]
    )

    route_share = (
        route_data
        .groupby("route")
        .size()
        .reset_index(name="Trips")
        .sort_values(
            "Trips",
            ascending=False
        )
    )

    top_routes = route_share.head(10)

    fig_route = px.pie(
        top_routes,
        names="route",
        values="Trips",
        title="Top 10 Route Share",
        hole=0.45,
        color_discrete_sequence=[
            GREEN_THEME["primary"],
            GREEN_THEME["secondary"],
            GREEN_THEME["dark"],
            GREEN_THEME["light"],
            GREEN_THEME["accent"],
        ],
    )

    fig_route.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(
            line=dict(
                color=COLORS["card"],
                width=2,
            )
        ),
    )

    fig_route = style_figure(fig_route)

    fig_route.update_layout(
        showlegend=True,
        legend=dict(
            font=dict(
                color=COLORS["text"]
            )
        ),
    )

    duration_data = filtered.copy()

    duration_data["duration_sec"] = (
        __import__("pandas")
        .to_numeric(
            duration_data["duration_sec"],
            errors="coerce"
        )
    )

    duration_data = duration_data.dropna(
        subset=["duration_sec"]
    )

    duration_data["duration_min"] = (
        duration_data["duration_sec"] / 60
    )

    fig_duration = px.histogram(
        duration_data,
        x="duration_min",
        nbins=30,
        title="Trip Duration Distribution",
        color_discrete_sequence=[
            GREEN_THEME["secondary"]
        ],
    )

    fig_duration.update_traces(
        marker_line_color=GREEN_THEME["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )

    if not duration_data.empty:
        median_duration = (
            duration_data["duration_min"]
            .median()
        )

        fig_duration.add_vline(
            x=median_duration,
            line_dash="dash",
            line_color=GREEN_THEME["accent"],
            line_width=2,
            annotation_text=(
                f"Median {median_duration:.1f} min"
            ),
            annotation_position="top",
        )

    fig_duration = style_figure(
        fig_duration,
        x_title="Duration (Minutes)",
        y_title="Count",
    )

    return (
        fig_station,
        fig_route,
        fig_duration,
    )

def create_stations_map(
    filtered,
    top_n=10
):
    if filtered.empty:
        fig = go.Figure()

        fig.update_layout(
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0,
            ),
            annotations=[
                dict(
                    text="No station data available",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(
                        size=18,
                        color=COLORS["muted_text"],
                    ),
                )
            ],
        )

        return fig

    station_data = (
        filtered
        .groupby(
            [
                "start_station_name",
                "start_station_latitude",
                "start_station_longitude",
            ],
            as_index=False,
        )
        .size()
        .rename(
            columns={
                "size": "trip_count"
            }
        )
    )

    station_data = station_data.dropna(
        subset=[
            "start_station_latitude",
            "start_station_longitude",
        ]
    )

    if station_data.empty:
        fig = go.Figure()

        fig.update_layout(
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0,
            ),
            annotations=[
                dict(
                    text="No station coordinates available",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(
                        size=18,
                        color=COLORS["muted_text"],
                    ),
                )
            ],
        )

        return fig

    try:
        top_n = int(top_n)
    except (TypeError, ValueError):
        top_n = 10

    top_n = max(1, top_n)

    station_data = (
        station_data
        .sort_values(
            "trip_count",
            ascending=False
        )
        .head(top_n)
    )

    fig = px.scatter_map(
        station_data,
        lat="start_station_latitude",
        lon="start_station_longitude",
        size="trip_count",
        color="trip_count",
        hover_name="start_station_name",
        hover_data={
            "trip_count": True,
            "start_station_latitude": False,
            "start_station_longitude": False,
        },
        color_continuous_scale=[
            GREEN_THEME["dark"],
            GREEN_THEME["secondary"],
            GREEN_THEME["primary"],
        ],
        size_max=35,
        zoom=11,
        center={
            "lat": 37.7749,
            "lon": -122.4194,
        },
        height=500,
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        coloraxis_showscale=False,
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
    )

    return fig