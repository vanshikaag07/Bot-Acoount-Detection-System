from pathlib import Path

import pandas as pd


def load_and_validate(file_path):
    """
    Load the bot-detection dataset and perform basic validation checks.

    Parameters:
        file_path: Location of the CSV dataset.

    Returns:
        The loaded pandas DataFrame.
    """

    # Load the CSV file into a pandas DataFrame.
    data = pd.read_csv(file_path)

    print("\nDATASET SIZE")
    print(f"Rows: {data.shape[0]:,}")
    print(f"Columns: {data.shape[1]}")

    # Check each column for missing values.
    print("\nMISSING VALUES")
    null_summary = pd.DataFrame({
        "Missing Count": data.isnull().sum(),
        "Missing Percent": (data.isnull().mean() * 100).round(2)
    })
    print(null_summary)

    # Check for duplicated User IDs.
    print("\nDUPLICATE USER ID CHECK")
    duplicate_user_ids = data["User ID"].duplicated().sum()
    print(f"Duplicate User IDs: {duplicate_user_ids:,}")

    # Confirm the Bot Label class balance.
    print("\nBOT LABEL CLASS BALANCE")
    label_counts = data["Bot Label"].value_counts().sort_index()
    label_percentages = (
        data["Bot Label"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    class_balance = pd.DataFrame({
        "Count": label_counts,
        "Percentage": label_percentages
    })

    print("0 = human account; 1 = bot account")
    print(class_balance)

    # Check whether each class is reasonably close to 50%.
    if label_percentages.between(45, 55).all():
        print("Result: The classes are approximately balanced.")
    else:
        print("Result: The classes are not approximately balanced.")

    # Print basic dataset summaries.
    print("\nDATASET INFORMATION")
    data.info()

    print("\nDESCRIPTIVE STATISTICS")
    print(data.describe(include="all"))

    return data


if __name__ == "__main__":
    project_folder = Path(__file__).resolve().parent
    dataset_path = project_folder / "data" / "bot_detection_data.csv"

    dataset = load_and_validate(dataset_path)