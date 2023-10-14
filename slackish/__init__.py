import re
import typing

import requests
import loguru


DEFAULT_CRUMB = (
    "s-1697303913-e50919428134e4d00f8d8e6a9a9e4f88241e8ccc35620b8ee1dee2450f148c80-☃"
)


def ensure_workspace_url(workspace_name_or_url: str) -> str:
    """
    Ensure the provided workspace name or URL ends with '.slack.com'.

    :param workspace_name_or_url: Workspace name or full URL.
    :return: Full workspace URL with '.slack.com' suffix.
    """
    if workspace_name_or_url.lower().endswith(".slack.com"):
        return workspace_name_or_url
    else:
        return workspace_name_or_url + ".slack.com"


def extract_json_fragment(json_fragment: str, param: str) -> typing.Optional[str]:
    """
    Extract a value from a given JSON fragment.

    :param json_fragment: JSON string fragment containing the value to extract.
    :param param: Name of the parameter to extract.

    :return: The extracted value or None if not found.
    """
    pattern = r'"' + param + '"\s*:\s*"([^"]+)"'
    match = re.search(pattern, json_fragment)
    if match:
        return match.group(1)
    else:
        return None


def extract_api_token(json_fragment: str) -> typing.Optional[str]:
    """
    Extract the API token from a given JSON fragment.

    :param json_fragment: JSON string fragment containing the API token.
    :return: Extracted API token or None if not found.
    """
    return extract_json_fragment(json_fragment=json_fragment, param="api_token")


def extract_slack_info(json_fragment: str) -> typing.Optional[str]:
    """
    Extract the team ID and logged-in user ID.

    :param json_fragment: JSON string fragment containing the value to extract.
    :return: Extracted Slack information or None if not found.
    """
    return {
        "team_id": extract_json_fragment(json_fragment=json_fragment, param="team_id"),
        "user_id": extract_json_fragment(json_fragment=json_fragment, param="user_id"),
    }


def login_slack(
    workspace: str,
    email: str,
    password: str,
    session: typing.Optional[requests.Session] = None,
    crumb: typing.Optional[str] = None,
) -> requests.Session:
    """
    Login to Slack using the provided workspace, email, and password.

    :param workspace: Workspace name or full URL.
    :param email: Email address for login.
    :param password: Password for login.
    :param crumb: Security checksum.

    :return: Authenticated session object.
    """
    # Ensure the workspace URL is correctly formatted
    workspace_url = ensure_workspace_url(workspace)

    # Create a new session if not already initialized
    if session is None:
        session = requests.Session()

    # Check crumb
    if crumb is None:
        crumb = DEFAULT_CRUMB

    # Logging the start of the login process
    loguru.logger.debug(f"Starting login process for workspace: {workspace_url}")

    # Submit the login page
    response1 = session.post(
        url=f"https://{workspace_url}/sign_in_with_password",
        headers={
            "Authority": workspace_url,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        },
        data={
            "signin": "1",
            "redir": "",
            "has_remember": "true",
            # TODO: Figure out how to extract this value (concatenation of ts, hash and character)
            # Generated in https://a.slack-edge.com/bv1-10/login-core.26147b7.primer.min.js
            "crumb": crumb,
            "remember": "remember",
            "email": email,
            "password": password,
        },
    )

    # Check the response (should include automatic redirection)
    if response1.status_code != 200:
        loguru.logger.error(
            "Login failed: Could not successfully submit the login form"
        )
        raise Exception("Login failed: Could not successfully submit the login form")

    # Logging successful form submission
    loguru.logger.info("Successfully submitted the login form")

    slack_auth_cookie = session.cookies.get("d")
    if slack_auth_cookie is None:
        loguru.logger.error(
            "Login failed: The authentication cookie was not properly set (xoxd-...)"
        )
        raise Exception(
            "Login failed: The authentication cookie was not properly set (xoxd-...)"
        )

    # Now retrieving the Slack API token
    response2 = session.get(url=f"https://{workspace_url}/")

    if response2.status_code != 200:
        loguru.logger.error("Login failed: Could not proceed after login")
        raise Exception("Login failed: Could not proceed after login")

    # Logging successful login
    loguru.logger.info(f"Successfully logged in to {workspace_url}")

    # Extract API token
    slack_api_token = extract_api_token(response2.text)

    # Extract workspace information
    slack_login_info = extract_slack_info(response2.text)

    # Check API token
    if slack_api_token is None:
        loguru.logger.error(
            "Login failed: The authentication token could not be extracted (xoxc-...)"
        )
        raise Exception(
            "Login failed: The authentication cookie was not properly set (xoxc-...)"
        )

    # Record information in session in ad-hoc way (until we do subclassing)
    session.workspace = workspace_url
    session.email = email
    session.password = password
    session.auth_token = slack_api_token
    session.auth_cookie = slack_auth_cookie
    session.ids = slack_login_info

    return session
