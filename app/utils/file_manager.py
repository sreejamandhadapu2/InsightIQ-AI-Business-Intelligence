"""
File Manager Utility

Provides helper methods to save and load DataFrames.
"""

from pathlib import Path

import pandas as pd


class FileManager:
    """
    Utility class for reading and writing files.
    """

    def __init__(self) -> None:

        self.base_path = Path("data/processed")

        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_dataframe(
        self,
        df: pd.DataFrame,
        filename: str,
    ) -> None:
        """
        Save DataFrame as CSV.
        """

        filepath = self.base_path / filename

        df.to_csv(filepath, index=False)

        print(f"✅ Saved: {filepath}")

    def load_dataframe(
        self,
        filename: str,
    ) -> pd.DataFrame:
        """
        Load DataFrame from CSV.
        """

        filepath = self.base_path / filename

        return pd.read_csv(filepath)