import pandas as pd
import os
from dash import Dash, html, Input, Output, State

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
    create_route_flow_map,
)

df = pd.read_csv(
    r"Ford_Go_Bike_Analysis\Part1-DataBase\cleaned_data.csv"
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
    suppress_callback_exceptions=True,
    assets_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"),
    assets_url_path="assets",
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
    Output("filters-panel", "style"),
    Input("filters-toggle-btn", "n_clicks"),
    State("filters-panel", "style"),
    prevent_initial_call=True,
)
def toggle_filters(n_clicks, current_style):
    current_style = dict(current_style or {})
    is_open = current_style.get("display") != "none"
    current_style["display"] = "none" if is_open else "block"
    return current_style
 
 
@app.callback(
    Output("kpi-total-trips", "children"),
    Output("kpi-avg-duration", "children"),
    Output("kpi-unique-bikes", "children"),
    Output("kpi-active-stations", "children"),
    Output("kpi-busiest-station", "children"),
    Output("gr1", "figure"),
    Output("gr5", "figure"),
    Output("gr6", "figure"),
    Output("gr13", "figure"),
    Output("gr15", "figure"),
    Output("gr7", "figure"),
    Output("gr8", "figure"),
    Output("gr9", "figure"),
    Output("gr14", "figure"),
    Output("gr17", "figure"),
    Output("gr18", "figure"),
    Output("gr10", "figure"),
    Output("gr11", "figure"),
    Output("gr12", "figure"),
    Output("stations-map", "figure"),
    Output("route-flow-map", "figure"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("day-filter", "value"),
    Input("Bike-share", "value"),
    Input("trip-duration-filter", "value"),
    Input("top-station-filter", "value"),
    Input("date-range-filter", "start_date"),
    Input("date-range-filter", "end_date"),
)
def update_dashboard(
    user_types,
    genders,
    age_groups,
    days,
    share,
    duration_range,
    top_station_n,
    start_date,
    end_date,
):
    filtered = filter_dataframe(
        df,
        user_types,
        genders,
        age_groups,
        days,
        share,
        duration_range,
        start_date,
        end_date,
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
 
    route_flow_map = create_route_flow_map(
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
        busiest_station = "N/A"
        active_stations = "0"
    else:
        if "duration_min" in filtered.columns:
            mean_duration = filtered["duration_min"].mean()
            avg_duration = int(mean_duration) if pd.notna(mean_duration) else "N/A"
        else:
            avg_duration = "N/A"

        unique_bikes_text = (
            str(filtered["bike_id"].nunique())
            if "bike_id" in filtered.columns
            else "N/A"
        )
        active_stations = (
            str(filtered["start_station_id"].nunique())
            if "start_station_id" in filtered.columns
            else "N/A"
        )
        if "start_station_name" in filtered.columns and not filtered["start_station_name"].dropna().empty:
            busiest_station = filtered["start_station_name"].mode().iloc[0]
        else:
            busiest_station = "N/A"

    return (
        total_trips,
        avg_duration,
        unique_bikes_text,
        active_stations,
        busiest_station,
        *overview_figures,
        *time_figures,
        *user_figures,
        *trip_figures,
        stations_map,
        route_flow_map,
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        port=3000,
    )

