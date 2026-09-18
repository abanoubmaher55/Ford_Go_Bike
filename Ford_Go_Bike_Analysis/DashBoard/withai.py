"""
Ford GoBike Interactive Dashboard
----------------------------------
A Dash + Plotly Express dashboard for exploring the Ford GoBike trip dataset.

Run with:
    python src/dash_gobike.py

The file is organized into clearly separated sections:
    1. Imports & paths
    2. Data loading
    3. Data preparation (derived columns)
    4. Theme / colors
    5. Reusable helper + chart functions
    6. Layout (header, sidebar, KPI cards, tabs with charts)
    7. Callbacks (filtering + reset)
    8. App entry point
"""

# ---------------------------------------------------------------------------
# 1. IMPORTS & PATHS
# ---------------------------------------------------------------------------
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, State

# Robust paths so the script works no matter where it's launched from.
# This file lives in .../Osama-EDA-Phase1/src/dash_gobike.py

# Make sure our own src folder is importable so "import preprocessing" works
# even if the script is launched from a different working directory.


# ---------------------------------------------------------------------------
# 2. DATA LOADING
# ---------------------------------------------------------------------------
def load_data():
    """
    Load the Ford GoBike dataset.

    Tries to use the user's own preprocessing.read_file() first (since that
    may already handle cleaning steps specific to this project). Falls back
    to a plain pd.read_csv() if the preprocessing module isn't available or
    doesn't behave as expected, so the dashboard never fails to start.
    """
    try:
        data = pd.read_csv("Ford_Go_Bike\Ford_Go_Bike_Analysis\Part1-DataBase (Omar)\cleaned_data.csv")
        return data
    except Exception as err:
        print(f"Falling back to pd.read_csv() because: {err}")
        return pd.read_csv(DATA_PATH)


df = load_data()


# ---------------------------------------------------------------------------
# 3. DATA PREPARATION (derived columns)
# ---------------------------------------------------------------------------
# Correct day-of-week / month ordering used across all charts.
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """Create any derived columns that don't already exist. Never destroys
    original columns; only adds new ones when missing."""
    data = data.copy()

    # Parse datetime columns if present.
    if "start_time" in data.columns:
        data["start_time"] = pd.to_datetime(data["start_time"], errors="coerce")
    if "end_time" in data.columns:
        data["end_time"] = pd.to_datetime(data["end_time"], errors="coerce")

    # Trip duration in minutes.
    if "trip_duration_min" not in data.columns and "duration_sec" in data.columns:
        data["trip_duration_min"] = data["duration_sec"] / 60

    # Hour of day.
    if "hour" not in data.columns and "start_time" in data.columns:
        data["hour"] = data["start_time"].dt.hour

    # Day of week (categorical, Monday -> Sunday order).
    if "day_of_week" not in data.columns and "start_time" in data.columns:
        data["day_of_week"] = data["start_time"].dt.day_name()
    if "day_of_week" in data.columns:
        data["day_of_week"] = pd.Categorical(
            data["day_of_week"], categories=DAY_ORDER, ordered=True
        )

    # Month name (categorical, Jan -> Dec order).
    if "month" not in data.columns and "start_time" in data.columns:
        data["month"] = data["start_time"].dt.month_name()
    if "month" in data.columns:
        data["month"] = pd.Categorical(
            data["month"], categories=MONTH_ORDER, ordered=True
        )

    # Age, calculated from the dataset's own year (not necessarily "today"),
    # so ages make sense for a Feb 2019 dataset rather than using the
    # current calendar year.
    if "age" not in data.columns and "member_birth_year" in data.columns:
        if "start_time" in data.columns and data["start_time"].notna().any():
            reference_year = int(data["start_time"].dt.year.mode()[0])
        else:
            reference_year = datetime.now().year
        data["age"] = reference_year - data["member_birth_year"]
        # Drop obviously invalid ages (data entry errors), keep as NaN.
        data.loc[(data["age"] < 10) | (data["age"] > 100), "age"] = pd.NA

    # Age group, built from age if it doesn't already exist.
    if "age_group" not in data.columns and "age" in data.columns:
        bins = [0, 18, 25, 35, 45, 55, 65, 120]
        labels = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        data["age_group"] = pd.cut(data["age"], bins=bins, labels=labels)

    return data


df = prepare_data(df)


# ---------------------------------------------------------------------------
# 4. THEME / COLORS
# ---------------------------------------------------------------------------
COLORS = {
    "background": "#F7FAF7",
    "primary": "#2E7D32",
    "secondary": "#43A047",
    "accent": "#66BB6A",
    "light": "#E8F5E9",
    "dark": "#1B5E20",
    "text": "#263238",
    "white": "#FFFFFF",
}

# A green sequence for charts that need multiple distinct colors.
GREEN_SEQUENCE = ["#1B5E20", "#2E7D32", "#43A047", "#66BB6A", "#81C784", "#A5D6A7"]

CARD_STYLE = {
    "backgroundColor": COLORS["white"],
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(27, 94, 32, 0.12)",
    "padding": "18px 20px",
    "marginBottom": "18px",
}

CHART_LAYOUT_DEFAULTS = dict(
    paper_bgcolor=COLORS["white"],
    plot_bgcolor=COLORS["white"],
    font_color=COLORS["text"],
    title_font_color=COLORS["dark"],
    margin=dict(l=40, r=20, t=50, b=40),
)


# ---------------------------------------------------------------------------
# 5. REUSABLE HELPER + CHART FUNCTIONS
# ---------------------------------------------------------------------------
def empty_fig(message="No data available for the selected filters"):
    """Return a blank figure with a friendly message, used whenever the
    filtered dataframe has zero rows so charts never crash."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=COLORS["dark"]),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        **CHART_LAYOUT_DEFAULTS,
    )
    return fig


def style_fig(fig, title=None):
    """Apply consistent green theme styling to any Plotly figure."""
    if title:
        fig.update_layout(title=title)
    fig.update_layout(**CHART_LAYOUT_DEFAULTS)
    return fig


def chart_trips_by_day(data):
    if data.empty or "day_of_week" not in data.columns:
        return empty_fig()
    counts = (
        data["day_of_week"].value_counts()
        .reindex(DAY_ORDER)
        .fillna(0)
        .reset_index()
    )
    counts.columns = ["day_of_week", "trips"]
    fig = px.bar(
        counts, x="day_of_week", y="trips",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"day_of_week": "Day of Week", "trips": "Number of Trips"},
    )
    return style_fig(fig, "Trips by Day of Week")


def chart_trips_by_hour(data):
    if data.empty or "hour" not in data.columns:
        return empty_fig()
    counts = data["hour"].value_counts().sort_index().reset_index()
    counts.columns = ["hour", "trips"]
    fig = px.line(
        counts, x="hour", y="trips", markers=True,
        color_discrete_sequence=[COLORS["dark"]],
        labels={"hour": "Hour of Day", "trips": "Number of Trips"},
    )
    return style_fig(fig, "Trips by Hour of Day")


def chart_user_type(data):
    if data.empty or "user_type" not in data.columns:
        return empty_fig()
    counts = data["user_type"].value_counts().reset_index()
    counts.columns = ["user_type", "trips"]
    fig = px.bar(
        counts, x="user_type", y="trips", color="user_type",
        color_discrete_sequence=GREEN_SEQUENCE,
        labels={"user_type": "User Type", "trips": "Number of Trips"},
    )
    fig.update_layout(showlegend=False)
    return style_fig(fig, "User Type Distribution")


def chart_gender(data):
    if data.empty or "member_gender" not in data.columns:
        return empty_fig()
    counts = data["member_gender"].value_counts().reset_index()
    counts.columns = ["gender", "trips"]
    fig = px.pie(
        counts, names="gender", values="trips", hole=0.45,
        color_discrete_sequence=GREEN_SEQUENCE,
    )
    return style_fig(fig, "Gender Distribution")


def chart_age_distribution(data):
    if data.empty or "age" not in data.columns or data["age"].dropna().empty:
        return empty_fig()
    fig = px.histogram(
        data.dropna(subset=["age"]), x="age", nbins=40,
        color_discrete_sequence=[COLORS["secondary"]],
        labels={"age": "Age"},
    )
    fig.update_yaxes(title_text="Number of Trips")
    return style_fig(fig, "Age Distribution")


def chart_duration_distribution(data):
    if data.empty or "trip_duration_min" not in data.columns:
        return empty_fig()
    clean = data.dropna(subset=["trip_duration_min"])
    if clean.empty:
        return empty_fig()
    # Clip extreme outliers (e.g. > 99th percentile) so the histogram stays readable.
    upper_limit = clean["trip_duration_min"].quantile(0.99)
    clipped = clean[clean["trip_duration_min"] <= upper_limit]
    fig = px.histogram(
        clipped, x="trip_duration_min", nbins=50,
        color_discrete_sequence=[COLORS["accent"]],
        labels={"trip_duration_min": "Trip Duration (minutes)"},
    )
    fig.update_yaxes(title_text="Number of Trips")
    return style_fig(fig, "Trip Duration Distribution (outliers trimmed at 99th percentile)")


def chart_avg_duration_by_user_type(data):
    if data.empty or "user_type" not in data.columns or "trip_duration_min" not in data.columns:
        return empty_fig()
    avg = data.groupby("user_type", observed=True)["trip_duration_min"].mean().reset_index()
    if avg.empty:
        return empty_fig()
    fig = px.bar(
        avg, x="user_type", y="trip_duration_min", color="user_type",
        color_discrete_sequence=GREEN_SEQUENCE,
        labels={"user_type": "User Type", "trip_duration_min": "Avg Duration (min)"},
    )
    fig.update_layout(showlegend=False)
    return style_fig(fig, "Average Trip Duration by User Type")


def chart_trips_by_month(data):
    if data.empty or "month" not in data.columns:
        return empty_fig()
    counts = (
        data["month"].value_counts()
        .reindex(MONTH_ORDER)
        .dropna()
        .reset_index()
    )
    counts.columns = ["month", "trips"]
    if counts.empty:
        return empty_fig()
    fig = px.bar(
        counts, x="month", y="trips",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"month": "Month", "trips": "Number of Trips"},
    )
    return style_fig(fig, "Trips by Month")


def _top_stations(data, id_col, name_col, top_n=10):
    if data.empty or name_col not in data.columns:
        return pd.DataFrame(columns=["station", "trips"])
    counts = data[name_col].value_counts().head(top_n).reset_index()
    counts.columns = ["station", "trips"]
    return counts


def chart_top_start_stations(data):
    counts = _top_stations(data, "start_station_id", "start_station_name")
    if counts.empty:
        return empty_fig()
    fig = px.bar(
        counts.sort_values("trips"), x="trips", y="station", orientation="h",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"trips": "Number of Trips", "station": "Start Station"},
    )
    return style_fig(fig, "Top 10 Start Stations")


def chart_top_end_stations(data):
    counts = _top_stations(data, "end_station_id", "end_station_name")
    if counts.empty:
        return empty_fig()
    fig = px.bar(
        counts.sort_values("trips"), x="trips", y="station", orientation="h",
        color_discrete_sequence=[COLORS["secondary"]],
        labels={"trips": "Number of Trips", "station": "End Station"},
    )
    return style_fig(fig, "Top 10 End Stations")


def chart_station_map(data):
    required = {
        "start_station_name", "start_station_latitude", "start_station_longitude",
    }
    if data.empty or not required.issubset(data.columns):
        return empty_fig()

    station_counts = (
        data.groupby(
            ["start_station_name", "start_station_latitude", "start_station_longitude"],
            observed=True,
        )
        .size()
        .reset_index(name="trips")
    )
    if station_counts.empty:
        return empty_fig()

    # Plotly >= 5.24 renamed scatter_mapbox to scatter_map (MapLibre-based,
    # no Mapbox token needed). Try the modern name first, fall back for
    # older Plotly installs.
    map_kwargs = dict(
        lat="start_station_latitude",
        lon="start_station_longitude",
        size="trips",
        color="trips",
        color_continuous_scale=["#A5D6A7", "#43A047", "#1B5E20"],
        hover_name="start_station_name",
        zoom=11,
        height=520,
    )
    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(station_counts, map_style="open-street-map", **map_kwargs)
    else:
        fig = px.scatter_mapbox(station_counts, mapbox_style="open-street-map", **map_kwargs)
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title="Station Activity Map (bubble size = trips)")
    fig.update_layout(paper_bgcolor=COLORS["white"], font_color=COLORS["text"])
    return fig


def chart_age_vs_duration(data):
    if data.empty or "age" not in data.columns or "trip_duration_min" not in data.columns:
        return empty_fig()
    clean = data.dropna(subset=["age", "trip_duration_min"])
    if clean.empty:
        return empty_fig()
    # Sample for performance if the filtered set is very large.
    if len(clean) > 5000:
        clean = clean.sample(5000, random_state=42)
    color_arg = "user_type" if "user_type" in clean.columns else None
    fig = px.scatter(
        clean, x="age", y="trip_duration_min", color=color_arg,
        color_discrete_sequence=GREEN_SEQUENCE, opacity=0.6,
        labels={"age": "Age", "trip_duration_min": "Trip Duration (min)"},
    )
    return style_fig(fig, "Age vs Trip Duration")


def chart_usertype_vs_avg_duration(data):
    return chart_avg_duration_by_user_type(data)  # same logic, reused


def chart_gender_vs_avg_duration(data):
    if data.empty or "member_gender" not in data.columns or "trip_duration_min" not in data.columns:
        return empty_fig()
    avg = data.groupby("member_gender", observed=True)["trip_duration_min"].mean().reset_index()
    if avg.empty:
        return empty_fig()
    fig = px.bar(
        avg, x="member_gender", y="trip_duration_min", color="member_gender",
        color_discrete_sequence=GREEN_SEQUENCE,
        labels={"member_gender": "Gender", "trip_duration_min": "Avg Duration (min)"},
    )
    fig.update_layout(showlegend=False)
    return style_fig(fig, "Average Trip Duration by Gender")


# ---------------------------------------------------------------------------
# 6. LAYOUT
# ---------------------------------------------------------------------------
app = Dash(__name__)
app.title = "Ford GoBike Interactive Dashboard"
server = app.server  # useful if deploying later (e.g. gunicorn)

# --- Filter option values, built dynamically from the real data ---
def safe_min_date(data):
    if "start_time" in data.columns and data["start_time"].notna().any():
        return data["start_time"].min().date()
    return datetime.now().date()


def safe_max_date(data):
    if "start_time" in data.columns and data["start_time"].notna().any():
        return data["start_time"].max().date()
    return datetime.now().date()


MIN_DATE = safe_min_date(df)
MAX_DATE = safe_max_date(df)

USER_TYPE_OPTIONS = sorted(df["user_type"].dropna().unique().tolist()) if "user_type" in df.columns else []
GENDER_OPTIONS = sorted(df["member_gender"].dropna().unique().tolist()) if "member_gender" in df.columns else []
AGE_GROUP_OPTIONS = (
    [g for g in ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
     if g in df["age_group"].dropna().unique().tolist()]
    if "age_group" in df.columns else []
)
DAY_OPTIONS = [d for d in DAY_ORDER if "day_of_week" in df.columns]


def build_checklist(component_id, options, default_all=True):
    """Small helper to keep checklist creation consistent + DRY."""
    return dcc.Checklist(
        id=component_id,
        options=[{"label": f" {opt}", "value": opt} for opt in options],
        value=options if default_all else [],
        labelStyle={"display": "block", "marginBottom": "4px", "color": COLORS["text"]},
        style={"marginBottom": "16px"},
    )


def sidebar():
    return html.Div(
        [
            html.H3("Filters", style={"color": COLORS["dark"], "marginBottom": "18px"}),

            html.Label("Date Range", style={"fontWeight": "600", "color": COLORS["dark"]}),
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=MIN_DATE,
                max_date_allowed=MAX_DATE,
                start_date=MIN_DATE,
                end_date=MAX_DATE,
                style={"marginBottom": "20px"},
            ),

            html.Label("User Type", style={"fontWeight": "600", "color": COLORS["dark"]}),
            build_checklist("user-type-filter", USER_TYPE_OPTIONS),

            html.Label("Gender", style={"fontWeight": "600", "color": COLORS["dark"]}),
            build_checklist("gender-filter", GENDER_OPTIONS),

            html.Label("Age Group", style={"fontWeight": "600", "color": COLORS["dark"]}),
            build_checklist("age-group-filter", AGE_GROUP_OPTIONS),

            html.Label("Day of Week", style={"fontWeight": "600", "color": COLORS["dark"]}),
            build_checklist("day-filter", DAY_OPTIONS),

            html.Button(
                "Reset Filters",
                id="reset-button",
                n_clicks=0,
                style={
                    "backgroundColor": COLORS["primary"],
                    "color": COLORS["white"],
                    "border": "none",
                    "borderRadius": "8px",
                    "padding": "10px 16px",
                    "cursor": "pointer",
                    "width": "100%",
                    "fontWeight": "600",
                    "marginTop": "10px",
                },
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


def kpi_card(title, value_id):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "13px", "color": COLORS["text"], "opacity": 0.75}),
            html.Div(id=value_id, style={"fontSize": "26px", "fontWeight": "700", "color": COLORS["dark"]}),
        ],
        style={**CARD_STYLE, "flex": "1", "textAlign": "center", "minWidth": "180px"},
    )


def kpi_row():
    return html.Div(
        [
            kpi_card("Total Trips", "kpi-total-trips"),
            kpi_card("Average Trip Duration (min)", "kpi-avg-duration"),
            kpi_card("Unique Bikes", "kpi-unique-bikes"),
            kpi_card("Most Popular Start Station", "kpi-popular-station"),
        ],
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "10px"},
    )


def chart_card(graph_id, half_width=True):
    return html.Div(
        dcc.Graph(id=graph_id, config={"displaylogo": False}),
        style={**CARD_STYLE, "flex": "1", "minWidth": "420px" if half_width else "100%"},
    )


def two_col_row(id_a, id_b):
    return html.Div(
        [chart_card(id_a), chart_card(id_b)],
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
    )


overview_tab = html.Div(
    [
        kpi_row(),
        two_col_row("chart-day-of-week", "chart-hour"),
        two_col_row("chart-user-type", "chart-gender"),
        two_col_row("chart-age-dist", "chart-duration-dist"),
        two_col_row("chart-avg-duration-usertype", "chart-month"),
    ]
)

station_tab = html.Div(
    [
        two_col_row("chart-top-start-stations", "chart-top-end-stations"),
        chart_card("chart-station-map", half_width=False),
    ]
)

behavior_tab = html.Div(
    [
        chart_card("chart-age-vs-duration", half_width=False),
        two_col_row("chart-usertype-vs-avgduration", "chart-gender-vs-avgduration"),
    ]
)


def header():
    return html.Div(
        [
            html.H1("🚲 Ford GoBike Interactive Dashboard", style={"color": COLORS["white"], "margin": "0"}),
            html.P(
                "Explore Ford GoBike trip patterns by time, station, and rider demographics. "
                "Use the filters on the left to drill into the data.",
                style={"color": COLORS["light"], "margin": "6px 0 0 0"},
            ),
        ],
        style={
            "backgroundColor": COLORS["dark"],
            "padding": "24px 30px",
            "borderRadius": "14px",
            "marginBottom": "20px",
        },
    )


app.layout = html.Div(
    [
        header(),
        html.Div(
            [
                sidebar(),
                html.Div(
                    [
                        dcc.Tabs(
                            id="main-tabs",
                            value="overview",
                            children=[
                                dcc.Tab(label="Overview", value="overview", children=overview_tab),
                                dcc.Tab(label="Station Analysis", value="stations", children=station_tab),
                                dcc.Tab(label="User Behavior", value="behavior", children=behavior_tab),
                            ],
                        ),
                    ],
                    style={"flex": "1", "minWidth": "0"},
                ),
            ],
            style={"display": "flex", "gap": "20px", "alignItems": "flex-start"},
        ),
    ],
    style={
        "backgroundColor": COLORS["background"],
        "padding": "24px",
        "fontFamily": "'Segoe UI', Arial, sans-serif",
        "minHeight": "100vh",
    },
)


# ---------------------------------------------------------------------------
# 7. CALLBACKS
# ---------------------------------------------------------------------------
def filter_dataframe(start_date, end_date, user_types, genders, age_groups, days):
    """Apply all sidebar filters to the global dataframe and return the result.
    Every filter is optional/defensive so missing columns never crash the app."""
    data = df.copy()

    if "start_time" in data.columns and start_date and end_date:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        data = data[(data["start_time"] >= start_dt) & (data["start_time"] <= end_dt)]

    # Note: we check "is not None" (not just truthy) so that a checklist with
    # everything unchecked (an empty list, which is falsy) correctly filters
    # the data down to zero rows instead of being skipped.
    if "user_type" in data.columns and user_types is not None:
        data = data[data["user_type"].isin(user_types)]

    if "member_gender" in data.columns and genders is not None:
        data = data[data["member_gender"].isin(genders)]

    if "age_group" in data.columns and age_groups is not None:
        data = data[data["age_group"].isin(age_groups)]

    if "day_of_week" in data.columns and days is not None:
        data = data[data["day_of_week"].isin(days)]

    return data


@app.callback(
    Output("kpi-total-trips", "children"),
    Output("kpi-avg-duration", "children"),
    Output("kpi-unique-bikes", "children"),
    Output("kpi-popular-station", "children"),
    Output("chart-day-of-week", "figure"),
    Output("chart-hour", "figure"),
    Output("chart-user-type", "figure"),
    Output("chart-gender", "figure"),
    Output("chart-age-dist", "figure"),
    Output("chart-duration-dist", "figure"),
    Output("chart-avg-duration-usertype", "figure"),
    Output("chart-month", "figure"),
    Output("chart-top-start-stations", "figure"),
    Output("chart-top-end-stations", "figure"),
    Output("chart-station-map", "figure"),
    Output("chart-age-vs-duration", "figure"),
    Output("chart-usertype-vs-avgduration", "figure"),
    Output("chart-gender-vs-avgduration", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("day-filter", "value"),
)
def update_dashboard(start_date, end_date, user_types, genders, age_groups, days):
    """Main callback: filters the data once, then builds every KPI and chart
    from that single filtered dataframe."""
    filtered = filter_dataframe(start_date, end_date, user_types, genders, age_groups, days)

    # --- KPIs (with safe defaults for the empty-data case) ---
    total_trips = len(filtered)

    if total_trips == 0:
        avg_duration_text = "N/A"
        unique_bikes_text = "0"
        popular_station_text = "N/A"
    else:
        avg_duration = (
            filtered["trip_duration_min"].mean()
            if "trip_duration_min" in filtered.columns else None
        )
        avg_duration_text = f"{avg_duration:.1f}" if avg_duration is not None else "N/A"

        unique_bikes_text = (
            str(filtered["bike_id"].nunique()) if "bike_id" in filtered.columns else "N/A"
        )

        if "start_station_name" in filtered.columns and not filtered["start_station_name"].dropna().empty:
            popular_station_text = filtered["start_station_name"].value_counts().idxmax()
        else:
            popular_station_text = "N/A"

    # --- Charts ---
    figs = (
        chart_trips_by_day(filtered),
        chart_trips_by_hour(filtered),
        chart_user_type(filtered),
        chart_gender(filtered),
        chart_age_distribution(filtered),
        chart_duration_distribution(filtered),
        chart_avg_duration_by_user_type(filtered),
        chart_trips_by_month(filtered),
        chart_top_start_stations(filtered),
        chart_top_end_stations(filtered),
        chart_station_map(filtered),
        chart_age_vs_duration(filtered),
        chart_usertype_vs_avg_duration(filtered),
        chart_gender_vs_avg_duration(filtered),
    )

    return (
        f"{total_trips:,}",
        avg_duration_text,
        unique_bikes_text,
        popular_station_text,
        *figs,
    )


@app.callback(
    Output("date-range", "start_date"),
    Output("date-range", "end_date"),
    Output("user-type-filter", "value"),
    Output("gender-filter", "value"),
    Output("age-group-filter", "value"),
    Output("day-filter", "value"),
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    """Reset every filter back to its default (all-inclusive) state."""
    return MIN_DATE, MAX_DATE, USER_TYPE_OPTIONS, GENDER_OPTIONS, AGE_GROUP_OPTIONS, DAY_OPTIONS


# ---------------------------------------------------------------------------
# 8. APP ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
