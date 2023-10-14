def fetch_from_slack_api(session, endpoint, data, cursor=None, cursor_name="cursor"):
    """Fetch data from Slack API."""
    if cursor:
        data[cursor_name] = cursor

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


def list_data_using_endpoint(
    session, endpoint, key_in_response, initial_data, cursor_name="cursor"
):
    """Generic function to list data from Slack using a specified API endpoint."""
    all_data = []
    cursor = None

    while True:
        result = fetch_from_slack_api(
            session=session,
            endpoint=endpoint,
            data=initial_data,
            cursor=cursor,
            cursor_name=cursor_name,
        )

        if not result["ok"]:
            raise Exception(f"Could not fetch data from {endpoint}: " + result["error"])

        new_data = result[key_in_response]
        all_data.extend(new_data)

        cursor = result.get("next_{}".format(cursor_name))
        if not cursor or len(new_data) == 0:
            break

    return all_data
