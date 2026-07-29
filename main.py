# import the base agent classes and access the subclasses
#from agents.test_agent import TestAgent

#agent = TestAgent()

#result = agent.run()

#print(result)

#print(agent.health_check()) /*

# import the base agent - Collection Agent - classes and access the subclasses
from agents.collection_agent import CollectionAgent


###


agent = CollectionAgent()

df = agent.collect("data/sales.csv") # or "data/sales.xlsx" or "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=YOUR_API_KEY"

print(df)

print()

print(agent.health_check())