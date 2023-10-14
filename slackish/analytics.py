import slackish.helpers


def get_member_analytics(
    session,
    date_range="30d",
    count=500,
    sort_column="real_name",
    sort_direction="asc",
    query=None,
):
    data = {
        "token": session.auth_token,
        "date_range": date_range,
        "count": count,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        # "_x_reason": "loadMembersDataForTimeRange",
        # "_x_mode": "online",
    }
    return slackish.helpers.list_data_using_endpoint(
        session,
        "admin.analytics.getMemberAnalytics",
        "member_activity",
        data,
        "cursor_mark",
    )
