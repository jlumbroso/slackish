def list_invites_history(session):
    def lih_aux(cursor=None):
        data = {
            "token": session.auth_token,
            "type": "accepted",
            "sort_by": "date_create",
            "sort_dir": "DESC",
            # "_x_reason": "fetch_invites_history_admin",
            # "_x_mode": "online",
        }
        if cursor is not None:
            data["cursor"] = cursor

        response = session.post(
            url="https://{}/api/users.admin.fetchInvitesHistory".format(
                session.workspace
            ),
            params={
                "fp": "2d",
                "slack_route": session.ids.get("team_id"),
                # "_x_id": "74293f22-1697225176.572",
                # "_x_version_ts": "noversion",
            },
            headers={
                "Authority": session.workspace,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            },
            data=data,
        )
        if response.status_code != 200:
            raise Exception("Could not list invites history: " + response.text)

        result = response.json()

        return result

    invites = []
    cursor = None
    while True:
        result = lih_aux(cursor=cursor)
        if not result["ok"]:
            raise Exception("Could not list invites history: " + result["error"])

        # Add the current page of results to the list
        invites += result["invites"]

        # If there is a cursor, fetch the next page
        if result.get("next_cursor", None) is not None:
            cursor = result["next_cursor"]
        else:
            break

    return invites


def list_invite_requests(session):
    def lih_aux(cursor=None):
        data = {
            "token": session.auth_token,
            # "type": "accepted",
            "sort_by": "date_create",
            "sort_dir": "DESC",
            # "_x_reason": "fetch_invites_history_admin",
            # "_x_mode": "online",
        }
        if cursor is not None:
            data["cursor"] = cursor

        response = session.post(
            url="https://{}/api/users.admin.fetchInviteRequests".format(
                session.workspace
            ),
            params={
                "fp": "2d",
                "slack_route": session.ids.get("team_id"),
                # "_x_id": "74293f22-1697225176.572",
                # "_x_version_ts": "noversion",
            },
            headers={
                "Authority": session.workspace,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            },
            data=data,
        )
        if response.status_code != 200:
            raise Exception("Could not list invites history: " + response.text)

        result = response.json()

        return result

    invites = []
    cursor = None
    while True:
        result = lih_aux(cursor=cursor)
        if not result["ok"]:
            raise Exception("Could not list invites history: " + result["error"])

        # Add the current page of results to the list
        invites += result["requests"]

        # If there is a cursor, fetch the next page
        if result.get("next_cursor", None) is not None:
            cursor = result["next_cursor"]
        else:
            break

    return invites
