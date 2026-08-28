import pandas as pd

from agents.cleaning_agent import CleaningAgent


# ---------------------------------------------------------
# Create sample dirty data
# ---------------------------------------------------------

df = pd.DataFrame({

    "Customer Name": [
        " John Smith ",
        "Jane Doe",
        " John Smith ",
        "Bob Jones"
    ],

    "Revenue ($)": [
        "5000",
        "7000",
        "5000",
        "9000"
    ],

    "Email Address": [
        "john@example.com",
        "jane@example.com",
        "john@example.com",
        None
    ]

})


# ---------------------------------------------------------
# Create Cleaning Agent
# ---------------------------------------------------------

agent = CleaningAgent()


# ---------------------------------------------------------
# Clean data
# ---------------------------------------------------------

cleaned_df = agent.clean(df)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n--- CLEANED DATA ---")

print(cleaned_df)


# ---------------------------------------------------------
# Display metrics
# ---------------------------------------------------------

print("\n--- AGENT METRICS ---")

print(agent.metrics)