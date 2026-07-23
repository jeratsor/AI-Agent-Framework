from agents.collection_agent import CollectionAgent


agent = CollectionAgent()


df = agent.collect(
    "data/sales.xlsx"
)


print(df.head())

print(agent.metrics)