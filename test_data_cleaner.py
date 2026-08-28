import pandas as pd

from utils.data_cleaner import DataCleaner


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
# Create cleaner
# ---------------------------------------------------------

cleaner = DataCleaner()


# ---------------------------------------------------------
# Profile original data
# ---------------------------------------------------------

print("\n--- ORIGINAL PROFILE ---")

profile = cleaner.profile(df)

print(profile)


# ---------------------------------------------------------
# Find missing values
# ---------------------------------------------------------

print("\n--- MISSING VALUES ---")

missing = cleaner.find_missing_values(df)

print(missing)


# ---------------------------------------------------------
# Find duplicates
# ---------------------------------------------------------

print("\n--- DUPLICATES ---")

duplicates = cleaner.find_duplicates(df)

print(duplicates)


# ---------------------------------------------------------
# Clean data
# ---------------------------------------------------------

print("\n--- CLEANED DATA ---")

cleaned_df = cleaner.clean(df)

print(cleaned_df)


# ---------------------------------------------------------
# Compare row counts
# ---------------------------------------------------------

print("\n--- ROW COUNT ---")

print(
    f"Before: {len(df)}"
)

print(
    f"After:  {len(cleaned_df)}"
)