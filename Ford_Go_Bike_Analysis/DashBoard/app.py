import pandas as pd

from dash import Dash, html, Input, Output

from components.colors import COLORS
from components.header import build_header
from components.sidebar import side_bar
from components.tabs import build_tabs

from utils.data_filter import filter_dataframe

from charts.overview import create_overview_charts
from charts.time_analysis import create_time_charts
from charts.user_analysis import create_user_charts
from charts.trip_analysis import (
    create_trip_charts,
    create_stations_map,
)

df = pd.read_csv(
    r"Ford_Go_Bike\Ford_Go_Bike_Analysis\Part1-DataBase (Omar)\cleaned_data.csv"
)

df["start_time"] = pd.to_datetime(
    df["start_time"],
    errors="coerce"
)

if "start_hour" not in df.columns:
    df["start_hour"] = df["start_time"].dt.hour

if "duration_min" not in df.columns:
    df["duration_min"] = (
        pd.to_numeric(
            df["duration_sec"],
            errors="coerce"
        ) / 60
    )

app = Dash(
    __name__,
    suppress_callback_exceptions=True
)

app.title = "Ford GoBike Analytics"

app.layout = html.Div(
    [
        build_header(),
        html.Div(
            [
                side_bar(df),
                html.Div(
                    [
                        build_tabs()
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
                "boxSizing": "border-box",
            },
        ),
    ],
    style={
        "backgroundColor": COLORS["background"],
        "minHeight": "100vh",
        "margin": "0",
        "padding": "0",
    },
)

@app.callback(
    Output("kpi-total-trips", "children"),
    Output("kpi-avg-duration", "children"),
    Output("kpi-unique-bikes", "children"),
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
    Output("gr12", "figure"),
    Output("stations-map", "figure"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("day-filter", "value"),
    Input("trip-duration-filter", "value"),
    Input("top-station-filter", "value"),
)
def update_dashboard(
    user_types,
    genders,
    age_groups,
    days,
    duration_range,
    top_station_n,
):
    filtered = filter_dataframe(
        df,
        user_types,
        genders,
        age_groups,
        days,
        duration_range,
    )

    overview_figures = create_overview_charts(filtered)
    time_figures = create_time_charts(filtered)
    user_figures = create_user_charts(filtered)
    trip_figures = create_trip_charts(filtered)

    stations_map = create_stations_map(
        filtered,
        top_n=(
            top_station_n
            if top_station_n
            else 10
        ),
    )

    total_trips = len(filtered)

    if total_trips == 0:
        unique_bikes_text = "0"
        avg_duration = "N/A"
    else:
        avg_duration = (
            int(filtered["duration_min"].mean())
            if "duration_min" in filtered.columns
            else None
        )

        unique_bikes_text = (
            str(filtered["bike_id"].nunique())
            if "bike_id" in filtered.columns
            else "N/A"
        )

    return (
        total_trips,
        avg_duration,
        unique_bikes_text,
        *overview_figures,
        *time_figures,
        *user_figures,
        *trip_figures,
        stations_map,
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        port=3000,
    )