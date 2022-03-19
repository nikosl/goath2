import os.path

import click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from goath2 import __version__

SCOPES: list[str] = ["https://mail.google.com/"]


@click.command()
@click.option(
    "--secret",
    "-s",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
    default="./credentials.json",
    help="credentials json",
    show_default=True,
)
@click.option(
    "--auth",
    "-a",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, writable=True, resolve_path=True
    ),
    default="./token.json",
    help="token json",
    show_default=True,
)
@click.option(
    "--token",
    "-t",
    is_flag=True,
    default=False,
    help="print token",
    show_default=True,
)
@click.version_option(version=__version__)
def main(secret: str, auth: str, token: bool) -> None:
    """Google api authentication."""

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(auth):
        creds = Credentials.from_authorized_user_file(auth, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(auth, "w") as tkn:
            tkn.write(creds.to_json())

    if token:
        click.echo(creds.token)
    else:
        click.echo(creds.to_json())
