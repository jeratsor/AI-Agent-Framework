from agents.collection_agent import CollectionAgent

agent = CollectionAgent()

#df = agent.collect("data/sample.db")
# * = """"


df = agent.collect(
    source="data/sample.db",
    query= """
    SELECT *
    FROM employees
    WHERE department = 'Finance'
    """
    )  


print(df)