import pandas as pd


class DataCleaner:

    def __init__(self):
        pass


    # =========================================================
    # PROFILE
    # =========================================================

    def profile(self, df: pd.DataFrame) -> dict:
        """
        Generate a basic data-quality profile.

        Returns information about:
        - Number of rows
        - Number of columns
        - Missing values
        - Duplicate rows
        - Data types
        """

        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "DataCleaner expects a pandas DataFrame."
            )


        profile = {

            "rows": len(df),

            "columns": len(df.columns),

            "missing_values": (
                df.isnull()
                .sum()
                .to_dict()
            ),

            "duplicate_rows": (
                df.duplicated()
                .sum()
            ),

            "data_types": (
                df.dtypes
                .astype(str)
                .to_dict()
            )
        }


        return profile


    # =========================================================
    # FIND MISSING VALUES
    # =========================================================

    def find_missing_values(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Return a summary of missing values by column.
        """

        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "DataCleaner expects a pandas DataFrame."
            )


        missing = df.isnull().sum()

        missing = missing[
            missing > 0
        ]


        result = pd.DataFrame({

            "missing_count": missing,

            "missing_percentage": (
                missing / len(df) * 100
            )

        })


        return result


    # =========================================================
    # FIND DUPLICATES
    # =========================================================

    def find_duplicates(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Return duplicate rows.
        """

        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "DataCleaner expects a pandas DataFrame."
            )


        return df[
            df.duplicated(
                keep=False
            )
        ]


    # =========================================================
    # STANDARDIZE COLUMN NAMES
    # =========================================================

    def standardize_column_names(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Standardize column names.

        Example:

        'Customer Name'
        → 'customer_name'
        """

        df = df.copy()


        df.columns = (

            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(
                " ",
                "_"
            )
            .str.replace(
                r"[^a-z0-9_]",
                "",
                regex=True
            )

        )


        return df


    # =========================================================
    # CLEAN WHITESPACE
    # =========================================================

    def clean_whitespace(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove unnecessary whitespace from
        string columns.
        """

        df = df.copy()


        for column in df.select_dtypes(
            include="object"
        ).columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
            )


        return df


    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    def remove_duplicates(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove duplicate rows.
        """

        df = df.copy()


        return df.drop_duplicates(
            ignore_index=True
        )


    # =========================================================
    # CONVERT DATA TYPES
    # =========================================================
    def convert_data_types(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Attempt to convert columns to appropriate
        pandas data types.

        Numeric conversion is attempted first.
        Datetime conversion is only attempted for
        columns whose values appear date-like.
        """

        df = df.copy()

        for column in df.columns:

            # -----------------------------------------
            # Skip columns that are already datetime
            # -----------------------------------------

            if pd.api.types.is_datetime64_any_dtype(
                df[column]
            ):
                continue


            # -----------------------------------------
            # Numeric conversion
            # -----------------------------------------

            numeric = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            non_null = df[column].notna().sum()

            if (
                non_null > 0
                and numeric.notna().sum()
                / non_null
                >= 0.95
            ):

                df[column] = numeric

                continue


            # -----------------------------------------
            # Datetime detection
            # -----------------------------------------

            if df[column].dtype != "object":
                continue


            sample = (
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
            )


            if sample.empty:
                continue


            # Only attempt datetime conversion when
            # the column actually looks date-like.

            date_keywords = (
                "date",
                "time",
                "year",
                "month",
                "day"
            )

            column_name = column.lower()


            looks_like_date_column = any(
                keyword in column_name
                for keyword in date_keywords
            )


            if not looks_like_date_column:
                continue


            datetime = pd.to_datetime(
                df[column],
                errors="coerce"
            )


            if (
                datetime.notna().sum()
                / non_null
                >= 0.95
            ):

                df[column] = datetime


        return df


    # =========================================================
    # CLEAN
    # =========================================================

    def clean(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Run the standard cleaning pipeline.
        """

        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "DataCleaner expects a pandas DataFrame."
            )


        cleaned_df = df.copy()


        # Standardize column names

        cleaned_df = (
            self.standardize_column_names(
                cleaned_df
            )
        )


        # Clean whitespace

        cleaned_df = (
            self.clean_whitespace(
                cleaned_df
            )
        )


        # Convert data types

        cleaned_df = (
            self.convert_data_types(
                cleaned_df
            )
        )


        # Remove duplicate rows

        cleaned_df = (
            self.remove_duplicates(
                cleaned_df
            )
        )


        return cleaned_df