import plotly.express as px

from components.cards import style_figure
from components.colors import GREEN_THEME

def create_overview_charts(filtered):
    duration_data = filtered.copy()

    duration_data["duration_min"] = (
        duration_data["duration_sec"] / 60
    )

    fig1 = px.histogram(
        duration_data,
        x="duration_min",
        nbins=30,
        title="Trip Duration Distribution",
        color_discrete_sequence=[
            GREEN_THEME["primary"]
        ],
    )

    fig1.update_traces(
        marker_line_color=GREEN_THEME["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )

    fig1 = style_figure(
        fig1,
        x_title="Trip Duration (Minutes)",
        y_title="Number of Trips",
    )

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
        marker_line_color=GREEN_THEME["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )

    fig2 = style_figure(
        fig2,
        x_title="Age",
        y_title="Number of Users",
    )

    user_counts = (
        filtered["user_type"]
        .value_counts()
        .reset_index()
    )

    user_counts.columns = [
        "user_type",
        "count",
    ]

    fig3 = px.bar(
        user_counts,
        x="user_type",
        y="count",
        title="Users by Type",
        color="user_type",
        color_discrete_sequence=[
            GREEN_THEME["primary"],
            GREEN_THEME["secondary"],
        ],
    )

    fig3.update_traces(
        marker_line_width=0,
    )

    fig3 = style_figure(
        fig3,
        x_title="User Type",
        y_title="Number of Users",
    )

    gender_counts = (
        filtered["member_gender"]
        .value_counts()
        .reset_index()
    )

    gender_counts.columns = [
        "member_gender",
        "count",
    ]

    fig4 = px.bar(
        gender_counts,
        x="member_gender",
        y="count",
        title="Users by Gender",
        color="member_gender",
        color_discrete_sequence=[
            GREEN_THEME["primary"],
            GREEN_THEME["secondary"],
            GREEN_THEME["dark"],
        ],
    )

    fig4.update_traces(
        marker_line_width=0,
    )

    fig4 = style_figure(
        fig4,
        x_title="Gender",
        y_title="Number of Users",
    )

    return (
        fig1,
        fig2,
        fig3,
        fig4,
    )