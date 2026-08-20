import os
import msal
import requests

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

    print("Authentication failed:")
    print(result)

    raise SystemExit


token = result["access_token"]


headers = {
    "Authorization": f"Bearer {token}"
}


# ------------------------------------------------
# Test 1: Get tenant root site
# ------------------------------------------------

url = (
    "https://graph.microsoft.com/v1.0"
    "/sites/root"
)


response = requests.get(
    url,
    headers=headers
)


print("ROOT SITE TEST")
print("Status:", response.status_code)
print(response.text)

print("-" * 60)


# ------------------------------------------------
# Test 2: Get target site by path
# ------------------------------------------------

url = (
    "https://graph.microsoft.com/v1.0"
    "/sites/"
    "jaja626returns.sharepoint.com:"
    "/sites/Communication"
)


response = requests.get(
    url,
    headers=headers
)


print("TARGET SITE TEST")
print("Status:", response.status_code)
print(response.text)

print("-" * 60)


# ------------------------------------------------
# Test 3: List sites
# ------------------------------------------------

url = (
    "https://graph.microsoft.com/v1.0"
    "/sites"
)


response = requests.get(
    url,
    headers=headers
)


print("LIST SITES TEST")
print("Status:", response.status_code)
print(response.text)