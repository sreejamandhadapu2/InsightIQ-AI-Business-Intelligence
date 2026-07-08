import pandas as pd

from app.utils.file_manager import FileManager


def main():

    fm = FileManager()

    df = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Name": ["A", "B", "C"],
        }
    )

    fm.save_dataframe(df, "sample.csv")

    loaded = fm.load_dataframe("sample.csv")

    print(loaded)


if __name__ == "__main__":
    main()