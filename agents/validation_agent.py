import pandas as pd

from agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Validation Agent",
            description="Validates cleaned data for quality and consistency."
        )


    def execute(self):
        """
        Required by BaseAgent.
        """
        return True


    def validate(
        self,
        df: pd.DataFrame,
        required_columns=None,
        numeric_columns=None
    ) -> dict:
        """
        Validate a DataFrame without modifying it.

        Returns a dictionary containing validation results.
        """

        self.logger.info("Starting data validation.")

        results = {
            "status": "PASS",
            "checks": {},
            "issues": []
        }

        # --------------------------------------------------
        # 1. Check whether DataFrame is empty
        # --------------------------------------------------

        if df.empty:

            results["status"] = "FAIL"

            results["checks"]["not_empty"] = False

            results["issues"].append(
                "DataFrame is empty."
            )

        else:

            results["checks"]["not_empty"] = True


        # --------------------------------------------------
        # 2. Check required columns
        # --------------------------------------------------

        if required_columns:

            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:

                results["status"] = "FAIL"

                results["checks"]["required_columns"] = False

                results["issues"].append(
                    f"Missing required columns: {missing_columns}"
                )

            else:

                results["checks"]["required_columns"] = True


        # --------------------------------------------------
        # 3. Check missing values
        # --------------------------------------------------

        missing_values = int(df.isna().sum().sum())

        results["checks"]["missing_values"] = missing_values

        if missing_values > 0:

            if results["status"] == "PASS":
                results["status"] = "WARNING"

            results["issues"].append(
                f"Data contains {missing_values} missing values."
            )


        # --------------------------------------------------
        # 4. Check duplicate rows
        # --------------------------------------------------

        duplicate_count = int(df.duplicated().sum())

        results["checks"]["duplicates"] = duplicate_count

        if duplicate_count > 0:

            if results["status"] == "PASS":
                results["status"] = "WARNING"

            results["issues"].append(
                f"Data contains {duplicate_count} duplicate rows."
            )


        # --------------------------------------------------
        # 5. Check numeric columns
        # --------------------------------------------------

        if numeric_columns:

            invalid_numeric_columns = []

            for column in numeric_columns:

                if column not in df.columns:
                    continue

                if not pd.api.types.is_numeric_dtype(df[column]):

                    invalid_numeric_columns.append(column)


            if invalid_numeric_columns:

                results["status"] = "FAIL"

                results["checks"]["numeric_columns"] = False

                results["issues"].append(
                    f"Non-numeric columns found where numeric data was expected: "
                    f"{invalid_numeric_columns}"
                )

            else:

                results["checks"]["numeric_columns"] = True


        # --------------------------------------------------
        # 6. Update agent metrics
        # --------------------------------------------------

        self.update_metric(
            "rows",
            len(df)
        )

        self.update_metric(
            "columns",
            len(df.columns)
        )

        self.update_metric(
            "missing_values",
            missing_values
        )

        self.update_metric(
            "duplicates",
            duplicate_count
        )

        self.update_metric(
            "validation_status",
            results["status"]
        )


        self.logger.info(
            f"Validation complete. Status: {results['status']}"
        )

        return results