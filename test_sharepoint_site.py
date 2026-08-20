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


# Replace this with your actual SharePoint site URL
site_url = "https://jaja626returns.sharepoint.com/"


parts = site_url.replace(
    "https://",
    ""
).split("/")


hostname = parts[0]

site_path = "/" + "/".join(parts[1:])


graph_url = (
    f"https://graph.microsoft.com/v1.0"
    f"/sites/{hostname}:{site_path}"
)


response = requests.get(
    graph_url,
    headers=headers
)


response.raise_for_status()


site = response.json()


print("SharePoint site found!")
print("Site name:", site["displayName"])
print("Site ID:", site["id"])