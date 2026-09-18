def filter_dataframe(
    df,
    user_types,
    genders,
    age_groups,
    days,
    duration_range=None,
):
    """
    Filter dataframe based on dashboard filters.
    """

    data = df.copy()


    # =====================================================
    # User Type
    # =====================================================

    if user_types:

        data = data[
            data["user_type"].isin(user_types)
        ]


    # =====================================================
    # Gender
    # =====================================================

    if genders:

        data = data[
            data["member_gender"].isin(genders)
        ]


    # =====================================================
    # Age Group
    # =====================================================

    if age_groups:

        data = data[
            data["age_group"].isin(age_groups)
        ]


    # =====================================================
    # Day
    # =====================================================

    if days:

        data = data[
            data["day_of_week"].isin(days)
        ]


    # =====================================================
    # Trip Duration
    # =====================================================

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