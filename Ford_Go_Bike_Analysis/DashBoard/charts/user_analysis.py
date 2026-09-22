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
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["dark"]
        ],
    )

    fig9.update_traces(
        marker_line_color=COLORS["dark"],
        marker_line_width=0.5,
        opacity=0.9,
    )
    fig9.update_layout(showlegend=False)

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
        title="Age Distribution by User Type",
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
        ],
    )

    fig14 = style_figure(
        fig14,
        x_title="Age",
        y_title="Number of Users"
        
    )

    fig14.update_traces(
        marker_line_color=COLORS["dark"],
        marker_line_width=0.5,
        
    )

 

    # ==========================================
    # fig11 (gr17): Gender Distribution by User Type
    # ==========================================
    gender_by_type = (
        filtered.groupby(["user_type", "member_gender"])
        .size()
        .reset_index(name="count")
    )

    fig11 = px.bar(
        gender_by_type,
        x="user_type",
        y="count",
        color="member_gender",
        title="Gender Distribution by User Type",
        barmode="stack",
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["dark"],
        ],
    )

    fig11.update_layout(
        legend=dict(
            font=dict(color=COLORS["text"])
        ),
    )

    fig11 = style_figure(
        fig11,
        x_title="User Type",
        y_title="Number of Users"
    )

    # ==========================================
    # fig12 (gr18): Trips by Age Group & Gender
    # ==========================================
    heatmap_data = (
        filtered.groupby(["age_group", "member_gender"])
        .size()
        .reset_index(name="trip_count")
    )

    heatmap_pivot = heatmap_data.pivot(
        index="age_group",
        columns="member_gender",
        values="trip_count"
    )

    fig12 = px.imshow(
        heatmap_pivot,
        title="Trips by Age Group & Gender",
        color_continuous_scale=[COLORS["card"], COLORS["primary"], COLORS["dark"]],
        labels=dict(x="Gender", y="Age Group", color="Trip Count"),
    )

    fig12 = style_figure(fig12)

    return (
        fig7,
        fig8,
        fig9,
        fig14,
        fig11,
        fig12,
    )