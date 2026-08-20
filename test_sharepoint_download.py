import os
from io import BytesIO

import msal
import requests
import pandas as pd

from dotenv import load_dotenv


load_dotenv()


# --------------------------------------------------
# Microsoft Graph authentication
# --------------------------------------------------

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


# --------------------------------------------------
# SharePoint information
# --------------------------------------------------

drive_id = (
    "b!o_6agyHRG0WZrjeGSmBIvCwVhvZ6ZihHnykNm-D-v7j8NkTDp7JBQ7RYnAePw6j_"
)

file_id = (
    "01XX3YTZQXXWSN7KCXIFBYC5NMRIIA3OXV"
)


# --------------------------------------------------
# Download file
# --------------------------------------------------

graph_url = (
    f"https://graph.microsoft.com/v1.0"
    f"/drives/{drive_id}"
    f"/items/{file_id}"
    f"/content"
)


response = requests.get(
    graph_url,
    headers=headers
)


response.raise_for_status()


print("File downloaded successfully!")

print(
    "Downloaded bytes:",
    len(response.content)
)


# --------------------------------------------------
# Convert Excel file to DataFrame
# --------------------------------------------------

df = pd.read_excel(
    BytesIO(response.content)
)


print()
print("DataFrame:")
print(df)


print()
print("Rows:", len(df))
print("Columns:", len(df.columns))