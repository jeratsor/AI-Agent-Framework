import os
import requests
import msal

from dotenv import load_dotenv


load_dotenv()


tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
client_id = os.getenv("SHAREPOINT_CLIENT_ID")
client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")


authority = (
    f"https://login.microsoftonline.com/"
    f"{tenant_id}"
)


app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)


result = app.acquire_token_for_client(
    scopes=[
        "https://graph.microsoft.com/.default"
    ]
)


if "access_token" not in result:
    raise RuntimeError(
        "Microsoft Graph authentication failed."
    )


access_token = result["access_token"]


headers = {
    "Authorization": f"Bearer {access_token}"
}


site_id = (
    "jaja626returns.sharepoint.com,"
    "839afea3-d121-451b-99ae-37864a6048bc,"
    "f686152c-667a-4728-9f29-0d9be0febfb8"
)


graph_url = (
    f"https://graph.microsoft.com/v1.0"
    f"/sites/{site_id}/drives"
)


response = requests.get(
    graph_url,
    headers=headers
)


response.raise_for_status()


drives = response.json()


print("Document libraries found:")
print()


for drive in drives["value"]:

    print(
        f"Name: {drive['name']}"
    )

    print(
        f"Drive ID: {drive['id']}"
    )

    print(
        f"Drive Type: {drive['driveType']}"
    )

    print("-" * 50)