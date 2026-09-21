def filter_dataframe(
    df,
    user_types,
    genders,
    age_groups,
    days,
    share,
    duration_range=None,
):
    data = df.copy()

    if not user_types or not genders or not age_groups or not days or not share:
        return df.iloc[0:0]

    if user_types:
        data = data[
            data["user_type"].isin(user_types)
        ]

    if genders:
        data = data[
            data["member_gender"].isin(genders)
        ]

    if age_groups:
        data = data[
            data["age_group"].isin(age_groups)
        ]

    if days:
        data = data[
            data["day_of_week"].isin(days)
        ]
    if share:
        data = data[
            data["bike_share_for_all_trip"].isin(share)
        ]

    if duration_range:
        min_duration = duration_range[0]
        max_duration = duration_range[1]

        data = data[
            data["duration_min"].between(
                min_duration,
                max_duration
            )
        ]

    return data