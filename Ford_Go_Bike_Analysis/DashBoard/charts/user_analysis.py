import plotly.express as px

from components.cards import style_figure
from components.colors import COLORS

def create_user_charts(filtered):
    fig7 = px.pie(
        filtered,
        names="user_type",
        title="User Type Distribution",
        hole=0.45,
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["dark"],
            COLORS["dark"],
        ],
    )

    fig7.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(
            line=dict(
                color=COLORS["card"],
                width=2,
            )
        ),
    )

    fig7.update_layout(
        showlegend=True,
        legend=dict(
            font=dict(
                color=COLORS["text"]
            )
        ),
    )

    fig7 = style_figure(fig7)

    fig8 = px.pie(
        filtered,
        names="member_gender",
        title="Gender Distribution",
        hole=0.45,
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["dark"],
            COLORS["dark"],
        ],
    )

    fig8.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(
            line=dict(
                color=COLORS["card"],
                width=2,
            )
        ),
    )

    fig8.update_layout(
        showlegend=True,
        legend=dict(
            font=dict(
                color=COLORS["text"]
            )
        ),
    )

    fig8 = style_figure(fig8)

    age_counts = (
        filtered["age_group"]
        .value_counts()
        .reset_index()
    )

    age_counts.columns = [
        "age_group",
        "count"
    ]

    fig9 = px.bar(
        age_counts,
        x="age_group",
        y="count",
        title="Users by Age Group",
        color_discrete_sequence=[
            COLORS["dark"]
        ],
    )

    fig9.update_traces(
        marker_color=COLORS["dark"],
        marker_line_color=COLORS["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )

    fig9 = style_figure(
        fig9,
        x_title="Age Group",
        y_title="Number of Users"
    )

    fig14 = px.histogram(
        filtered,
        x="users' age",
        color="user_type",
        opacity=0.6,
        barmode="overlay",
        title="Age Distribution by User Type"
    )

    fig14 = style_figure(
        fig14,
        x_title="Age",
        y_title="Number of Users"
    )

    fig14.update_traces(
        marker_color=COLORS["dark"],
        marker_line_color=COLORS["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )

    
    return (
        fig7,
        fig8,
        fig9,
        fig14
    )