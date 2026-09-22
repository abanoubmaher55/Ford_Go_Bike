from dash import html, dcc
from components.colors import COLORS, GREEN_THEME
from components.filters import build_dropdown

CARD_STYLE = {
    "backgroundColor": COLORS["sidebar"],
    "borderRadius": "14px",
    "border": f"1px solid {COLORS['border']}",
    "boxShadow": "0 4px 15px rgba(13, 92, 99, 0.12)",
    "padding": "18px 20px",
    "marginBottom": "18px",
    "boxSizing": "border-box",
}


def side_bar(df):

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

    share = sorted(
        df["bike_share_for_all_trip"].dropna().unique().tolist()
    )

    min_date = df["start_time"].min().date()
    max_date = df["start_time"].max().date()

    duration_minutes = df["duration_sec"] / 60

    max_duration = int(
        duration_minutes.quantile(0.99)
    )

    max_duration = max(max_duration, 10)

    return html.Div(
        [
            html.H3(
                "Filters",
                style={
                    "color": COLORS["primary"],
                    "marginBottom": "20px",
                    "fontSize": "20px",
                    "fontWeight": "700",
                    "letterSpacing": "0.3px",
                },
            ),

            html.Label(
                "Date Range",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "10px",
                    "marginTop": "20px",
                    "display": "block",
                },
            ),
            dcc.DatePickerRange(
                id="date-range-filter",
                number_of_months_shown=1,
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                display_format="DD/MM/YYYY",
                start_date_placeholder_text="From",
                end_date_placeholder_text="To",
                style={"marginBottom": "10px"}
            ),
            html.Label(
                "User Type",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "8px",
                    "display": "block",
                },
            ),

            build_dropdown(
                "user-type-filter",
                USER_TYPE_OPTIONS,
            ),

            html.Label(
                "Gender",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "8px",
                    "marginTop": "16px",
                    "display": "block",
                },
            ),

            build_dropdown(
                "gender-filter",
                GENDER_OPTIONS,
            ),

            html.Label(
                "Age Group",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "8px",
                    "marginTop": "16px",
                    "display": "block",
                },
            ),

            build_dropdown(
                "age-group-filter",
                AGE_GROUP_OPTIONS,
            ),

            html.Label(
                "Day of Week",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "8px",
                    "marginTop": "16px",
                    "display": "block",
                },
            ),

            build_dropdown(
                "day-filter",
                DAYS,
            ),
            html.Label(
                "Bike Share",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "8px",
                    "marginTop": "16px",
                    "display": "block",
                },
            ),

            build_dropdown(
                "Bike-share",
                share,
            ),

            html.Label(
                "Trip Duration (Minutes)",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "10px",
                    "marginTop": "20px",
                    "display": "block",
                },
            ),

            dcc.RangeSlider(
                id="trip-duration-filter",
                min=0,
                max=max_duration,
                step=1,
                value=[0, 60],
                tooltip={
                    "placement": "bottom",
                    "always_visible": True,
                },
                marks={
                    0: "0",
                    max_duration: f"{max_duration} min",
                },
                updatemode="mouseup",
                className="custom-slider",
            ),

            html.Label(
                "Top Stations",
                style={
                    "fontWeight": "600",
                    "color": COLORS["text"],
                    "marginBottom": "10px",
                    "marginTop": "30px",
                    "display": "block",
                },
            ),

            dcc.Slider(
                id="top-station-filter",
                min=1,
                max=50,
                step=1,
                value=50,
                marks={
                    1: "1",
                    10: "10",
                    20: "20",
                    30: "30",
                    40: "40",
                    50: "50",
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True,
                },
                updatemode="mouseup",
                className="custom-slider",
            ),
        ],
        id="filters-panel",
        style={
            **CARD_STYLE,
            "width": "260px",
            "minWidth": "260px",
            "height": "fit-content",
            "position": "sticky",
            "top": "20px",
            "display": "none",
            "zIndex": 1000,
        },
    )
