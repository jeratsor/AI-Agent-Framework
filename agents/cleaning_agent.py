import pandas as pd

from agents.base_agent import BaseAgent
from utils.data_cleaner import DataCleaner
from utils.header_detector import HeaderDetector


class CleaningAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Cleaning Agent",
            description="Cleans and standardizes collected data."
        )

        self.cleaner = DataCleaner()
        self.detector = HeaderDetector()


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(self):

        """
        Required by BaseAgent.
        """

        return True


    # =========================================================
    # APPLY HEADER
    # Detect and apply the correct header row.
    # =========================================================

    def _apply_header(
        self,
        df: pd.DataFrame
    ) -> tuple[pd.DataFrame, int]:

        header_row = self.detector.detect(df)

        self.logger.info(
            f"Detected header row: {header_row}"
        )

        header = df.iloc[header_row]

        cleaned_df = df.iloc[header_row + 1:].copy()

        cleaned_df.columns = [
            str(column).strip()
            if pd.notna(column)
            else f"unnamed_{index}"
            for index, column in enumerate(header)
        ]

        cleaned_df.reset_index(
            drop=True,
            inplace=True
        )

        return cleaned_df, header_row


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
        # Record raw input metrics
        # -----------------------------------------

        rows_before = len(df)

        columns_before = len(df.columns)


        # -----------------------------------------
        # Header detection and application
        # -----------------------------------------

        df, header_row = self._apply_header(df)


        rows_after_header = len(df)


        # -----------------------------------------
        # Profile data after header application
        # -----------------------------------------

        profile = self.cleaner.profile(
            df
        )


        duplicates_found = profile[
            "duplicate_rows"
        ]


        missing_values = sum(
            profile[
                "missing_values"
            ].values()
        )


        # -----------------------------------------
        # Record initial metrics
        # -----------------------------------------

        self.update_metric(
            "rows_before",
            int(rows_before)
        )

        self.update_metric(
            "columns_before",
            int(columns_before)
        )

        self.update_metric(
            "header_row",
            int(header_row)
        )

        self.update_metric(
            "rows_after_header",
            int(rows_after_header)
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


        # -----------------------------------------
        # Calculate actual duplicate removal
        # -----------------------------------------

        duplicates_removed = (
            rows_after_header
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

        self.logger.info(
            f"Cleaning complete. "
            f"Raw rows: {rows_before} -> "
            f"After header: {rows_after_header} -> "
            f"After cleaning: {rows_after}"
        )

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