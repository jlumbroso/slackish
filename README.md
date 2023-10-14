# slackish

A Python module to access Slack's API from user-space, to circumvent all the artificial API limitations put in by greedy Salesforce. 🤑

## Why `slackish`?

While there exists an official Slack client for Python, Salesforce has introduced arbitrary restrictions on which API calls can be made based on different plans. This puts developers in a challenging position, as there's uncertainty regarding which API calls can be relied upon when building applications for others. `slackish` aims to provide a more reliable, robust, and less selective base for developers to build upon.

## Installation

```bash
pip install slackish
```

## Usage

Here's a basic example of how to use `slackish`:

```python
import slackish

session = slackish.login_slack(
    workspace="YOUR_WORKSPACE_NAME_OR_URL",
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD"
)

print("Slack workspace: ", session.workspace)
print("Slack cookie:    ", session.auth_cookie)
print("Slack token:     ", session.auth_token)
```

Replace `YOUR_WORKSPACE_NAME_OR_URL`, `YOUR_EMAIL`, and `YOUR_PASSWORD` with your actual credentials.

## Features

- Bypass Salesforce's artificial API limitations.
- Reliable and consistent access to Slack's API.
- User-friendly interface for easy integration.

## Contributing

We welcome contributions! Please check out our [GitHub repository](https://github.com/jlumbroso/slackish) for more details.

The next milestone is to wrap the functionality in a sub-class `requests.Session()` that automatically injects the authentication cookie/token when appropriate.

## Disclaimer

Please ensure you're adhering to Slack's Terms of Service when using this package. The maintainers of `slackish` are not responsible for any misuse or violation of terms.

## License

This project is licensed under [The Unlicense](https://unlicense.org/).
It means you can do anything you want with this, for whatever purposes, you don't
have to credit me, this project, or anything.


