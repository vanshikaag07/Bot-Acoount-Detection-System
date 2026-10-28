import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(df):
    # split into 70% train and 30% temp set
    # stratify on bot label so classes stay balanced
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=42,
        stratify=df['Bot Label']
    )
    
    # split the remaining 30% evenly into val (15%) and test (15%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=42,
        stratify=temp_df['Bot Label']
    )
    
    return train_df, val_df, test_df
