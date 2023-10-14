def fetch_from_slack_api(session, endpoint, data, cursor=None):
    """Fetch data from Slack API."""
    if cursor:
        data["cursor"] = cursor

    response = session.post(
        url=f"https://{session.workspace}/api/{endpoint}",
        params={
            "fp": "2d",
            "slack_route": session.ids.get("team_id"),
        },
        headers={
            "Authority": session.workspace,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        },
        data=data,
    )

    if response.status_code != 200:
        raise Exception(f"Could not fetch data from {endpoint}: " + response.text)

    return response.json()


def list_data_using_endpoint(session, endpoint, key_in_response, initial_data):
    """Generic function to list data from Slack using a specified API endpoint."""
    all_data = []
    cursor = None

    while True:
        result = fetch_from_slack_api(session, endpoint, initial_data, cursor)

        if not result["ok"]:
            raise Exception(f"Could not fetch data from {endpoint}: " + result["error"])

        all_data.extend(result[key_in_response])

        cursor = result.get("next_cursor")
        if not cursor:
            break

    return all_data


def list_invites_history(session):
    data = {
        "token": session.auth_token,
        "type": "accepted",
        "sort_by": "date_create",
        "sort_dir": "DESC",
    }
    return list_data_using_endpoint(
        session, "users.admin.fetchInvitesHistory", "invites", data
    )


def list_invite_requests(session):
    data = {
        "token": session.auth_token,
        "sort_by": "date_create",
        "sort_dir": "DESC",
    }
    return list_data_using_endpoint(
        session, "users.admin.fetchInviteRequests", "requests", data
    )
