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


drive_id = (
    "b!o_6agyHRG0WZrjeGSmBIvCwVhvZ6ZihHnykNm-D-v7j8NkTDp7JBQ7RYnAePw6j_"
)


graph_url = (
    f"https://graph.microsoft.com/v1.0"
    f"/drives/{drive_id}/root/children"
)


response = requests.get(
    graph_url,
    headers=headers
)


response.raise_for_status()


items = response.json()


print("Items in Documents:")
print()


for item in items["value"]:

    item_type = (
        "FOLDER"
        if "folder" in item
        else "FILE"
    )

    print(
        f"{item_type}: {item['name']}"
    )

    print(
        f"Item ID: {item['id']}"
    )

    print("-" * 50)