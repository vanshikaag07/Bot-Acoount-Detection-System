"""
Person 2: Feature engineering

Adds two engineered columns to the dataset:
  1. account_age_days — how old the account was, in days, relative to
     the dataset's own max "Created At" date (since we don't have a
     real "today" to compare against for historical data).
  2. retweet_follower_ratio — Retweet Count / Follower Count, with
     divide-by-zero handled for accounts with 0 followers.

Usage:
    from feature_engineering import add_features
    df = add_features(df)
"""

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- Feature 1: account age in days ---
    df["Created At"] = pd.to_datetime(df["Created At"], errors="coerce")
    reference_date = df["Created At"].max()
    df["account_age_days"] = (reference_date - df["Created At"]).dt.days

    # --- Feature 2: retweet-to-follower ratio ---
    # Replace 0 followers with NA so we don't divide by zero, then
    # fill the resulting NaNs (from 0 followers OR missing data) with 0.
    safe_followers = df["Follower Count"].replace(0, pd.NA)
    df["retweet_follower_ratio"] = df["Retweet Count"] / safe_followers
    df["retweet_follower_ratio"] = df["retweet_follower_ratio"].fillna(0)

    return df


if __name__ == "__main__":
    # Quick manual test — point this at your actual CSV once you have it.
    DATA_PATH = "../data/primary_dataset.csv"

    df = pd.read_csv(DATA_PATH)
    print("Before:", df.shape, "columns:", list(df.columns))

    df = add_features(df)

    print("\nAfter:", df.shape, "columns:", list(df.columns))
    print("\nNew columns preview:")
    print(df[["Created At", "account_age_days", "Retweet Count", "Follower Count", "retweet_follower_ratio"]].head())