import pandas as pd

from agents.base_agent import BaseAgent
from utils.data_cleaner import DataCleaner


class CleaningAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Cleaning Agent",
            description="Cleans and standardizes collected data."
        )

        self.cleaner = DataCleaner()


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(self):

        """
        Required by BaseAgent.
        """

        return True


    # =========================================================
    # CLEAN
    # =========================================================

    def clean(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        self.logger.info(
            "Starting data cleaning."
        )


        # -----------------------------------------
        # Validate input
        # -----------------------------------------

        if not isinstance(
            df,
            pd.DataFrame
        ):

            raise TypeError(
                "CleaningAgent expects a pandas DataFrame."
            )


        # -----------------------------------------
        # Profile original data
        # -----------------------------------------

        profile = self.cleaner.profile(
            df
        )


        # -----------------------------------------
        # Record initial metrics
        # -----------------------------------------

        rows_before = profile["rows"]

        columns_before = profile["columns"]

        duplicates_found = profile[
            "duplicate_rows"
        ]


        missing_values = sum(
            profile[
                "missing_values"
            ].values()
        )


        self.update_metric(
            "rows_before",
            int(rows_before)
        )

        self.update_metric(
            "columns_before",
            int(columns_before)
        )

        self.update_metric(
            "duplicates_found",
            int(duplicates_found)
        )

        self.update_metric(
            "missing_values_found",
            int(missing_values)
        )


        # -----------------------------------------
        # Run cleaning pipeline
        # -----------------------------------------

        cleaned_df = self.cleaner.clean(
            df
        )


        # -----------------------------------------
        # Calculate cleaning results
        # -----------------------------------------

        rows_after = len(
            cleaned_df
        )

        columns_after = len(
            cleaned_df.columns
        )


        duplicates_removed = (
            rows_before
            - rows_after
        )


        # -----------------------------------------
        # Record final metrics
        # -----------------------------------------

        self.update_metric(
            "rows_after",
            int(rows_after)
        )

        self.update_metric(
            "columns_after",
            int(columns_after)
        )

        self.update_metric(
            "duplicates_removed",
            int(duplicates_removed)
        )


        # -----------------------------------------
        # Log results
        # -----------------------------------------

        self.logger.info(f"Cleaning complete. "f"Rows: {rows_before} -> {rows_after}")

        self.logger.info(
            f"Duplicates found: "
            f"{duplicates_found}"
        )

        self.logger.info(
            f"Duplicates removed: "
            f"{duplicates_removed}"
        )

        self.logger.info(
            f"Missing values found: "
            f"{missing_values}"
        )


        return cleaned_df