import os
from dotenv import load_dotenv

from agents.collection_agent import CollectionAgent

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

"""url = (
    "https://api.openweathermap.org/data/2.5/weather"
    "?q=St.%20John's,CA"
    f"&appid={api_key}"
    "&units=metric"
)

OR for no API websites

url = (f"https://api.open-meteo.com/v1/forecast?latitude=47.56&longitude=-52.71&hourly=temperature_2m")

"""

url = (f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={api_key}")

agent = CollectionAgent()

df = agent.collect(url)

print(df)

print(api_key)