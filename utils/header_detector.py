import pandas as pd


class HeaderDetector:
    """
    Detects the most likely header row in a tabular DataFrame.
    """

    def detect(self, df: pd.DataFrame, max_rows: int = 15) -> int:
        """
        Detect the most likely header row.

        Returns:
            Zero-based row index of the detected header.
        """

        if df.empty:
            raise ValueError("Cannot detect a header in an empty DataFrame.")

        preview = df.head(max_rows)

        best_row = 0
        best_score = -1

        for row_index, row in preview.iterrows():

            values = [
                str(value).strip()
                for value in row
                if pd.notna(value) and str(value).strip()
            ]

            if not values:
                continue

            # Number of populated cells
            non_empty_count = len(values)

            # Headers should generally contain unique column names
            unique_count = len(set(values))

            # Penalize obvious metadata rows
            metadata_words = [
                "note",
                "as of date",
                "user id"
            ]

            metadata_count = sum(
                1
                for value in values
                if value.lower() in metadata_words
            )

            # Calculate score
            score = (
                non_empty_count * 2
                + unique_count
                - metadata_count * 5
            )

            # Prefer rows containing several columns
            if non_empty_count >= 3:
                score += 5

            if score > best_score:
                best_score = score
                best_row = row_index

        return best_row