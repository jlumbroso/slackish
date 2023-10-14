import slackish.helpers


def list_invites_history(session):
    data = {
        "token": session.auth_token,
        "type": "accepted",
        "sort_by": "date_create",
        "sort_dir": "DESC",
    }
    return slackish.helpers.list_data_using_endpoint(
        session, "users.admin.fetchInvitesHistory", "invites", data
    )


def list_invite_requests(session):
    data = {
        "token": session.auth_token,
        "sort_by": "date_create",
        "sort_dir": "DESC",
    }
    return slackish.helpers.list_data_using_endpoint(
        session, "users.admin.fetchInviteRequests", "requests", data
    )
