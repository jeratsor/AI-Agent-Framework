import pandas as pd
from agents.collection_agent import CollectionAgent

import os
from dotenv import load_dotenv

load_dotenv()

print("SITE URL:", os.getenv("SHAREPOINT_SITE_URL"))

agent = CollectionAgent()

df = agent.collect(
    source="sharepoint",
    file_path="personal folder/KPI.db",
)

print(df)