from dash import html, dcc

from components.colors import COLORS, GREEN_THEME
from components.filters import build_checklist


# =========================================================
# Sidebar Card Style
# =========================================================

CARD_STYLE = {

    "backgroundColor":
        COLORS["sidebar"],

    "borderRadius":
        "14px",

    "border":
        f"1px solid {COLORS['border']}",

    "boxShadow":
        "0 4px 15px rgba(13, 92, 99, 0.12)",

    "padding":
        "18px 20px",

    "marginBottom":
        "18px",

    "boxSizing":
        "border-box",
}


def side_bar(df):

    """
    Build dashboard sidebar with filters.
    """

    # =====================================================
    # User Type
    # =====================================================

    USER_TYPE_OPTIONS = sorted(
        df["user_type"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================================
    # Gender
    # =====================================================

    GENDER_OPTIONS = sorted(
        df["member_gender"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================================
    # Age Group
    # =====================================================

    AGE_GROUP_OPTIONS = sorted(
        df["age_group"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================================
    # Days
    # =====================================================

    DAYS = sorted(
        df["day_of_week"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================================
    # Trip Duration
    # =====================================================

    duration_minutes = (
        df["duration_sec"] / 60
    )

    max_duration = int(
        duration_minutes.quantile(0.99)
    )

    max_duration = max(
        max_duration,
        10
    )

    # =====================================================
    # Sidebar
    # =====================================================

    return html.Div(

        [

            # =================================================
            # Title
            # =================================================

            html.H3(
                "Filters",

                style={
                    "color":
                        COLORS["primary"],

                    "marginBottom":
                        "20px",

                    "fontSize":
                        "20px",

                    "fontWeight":
                        "700",

                    "letterSpacing":
                        "0.3px",
                },
            ),

            # =================================================
            # User Type
            # =================================================

            html.Label(
                "User Type",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "8px",

                    "display":
                        "block",
                },
            ),

            build_checklist(
                "user-type-filter",
                USER_TYPE_OPTIONS,
            ),

            # =================================================
            # Gender
            # =================================================

            html.Label(
                "Gender",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "8px",

                    "marginTop":
                        "16px",

                    "display":
                        "block",
                },
            ),

            build_checklist(
                "gender-filter",
                GENDER_OPTIONS,
            ),

            # =================================================
            # Age Group
            # =================================================

            html.Label(
                "Age Group",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "8px",

                    "marginTop":
                        "16px",

                    "display":
                        "block",
                },
            ),

            build_checklist(
                "age-group-filter",
                AGE_GROUP_OPTIONS,
            ),

            # =================================================
            # Day of Week
            # =================================================

            html.Label(
                "Day of Week",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "8px",

                    "marginTop":
                        "16px",

                    "display":
                        "block",
                },
            ),

            build_checklist(
                "day-filter",
                DAYS,
            ),

            # =================================================
            # Trip Duration
            # =================================================

            html.Label(
                "Trip Duration (Minutes)",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "10px",

                    "marginTop":
                        "20px",

                    "display":
                        "block",
                },
            ),

            dcc.RangeSlider(

                id="trip-duration-filter",

                min=0,

                max=max_duration,

                step=1,

                value=[
                    0,
                    max_duration
                ],

                tooltip={
                    "placement":
                        "bottom",

                    "always_visible":
                        True,
                },

                marks={
                    0: "0",

                    max_duration:
                        f"{max_duration} min",
                },

                updatemode="mouseup",

                className="custom-slider",
            ),

            # =================================================
            # Top Station
            # =================================================

            html.Label(
                "Top Stations",

                style={
                    "fontWeight":
                        "600",

                    "color":
                        COLORS["text"],

                    "marginBottom":
                        "10px",

                    "marginTop":
                        "30px",

                    "display":
                        "block",
                },
            ),

            dcc.Slider(

                id="top-station-filter",

                min=1,

                max=50,

                step=1,

                value=10,

                marks={
                    1: "1",
                    10: "10",
                    20: "20",
                    30: "30",
                    40: "40",
                    50: "50",
                },

                tooltip={
                    "placement":
                        "bottom",

                    "always_visible":
                        True,
                },

                updatemode="mouseup",

                className="custom-slider",
            ),

        ],

        style={
            **CARD_STYLE,

            "width":
                "260px",

            "minWidth":
                "260px",

            "height":
                "fit-content",

            "position":
                "sticky",

            "top":
                "20px",
        },
    )