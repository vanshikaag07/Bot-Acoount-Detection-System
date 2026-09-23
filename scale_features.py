import pandas as pd
from sklearn.preprocessing import StandardScaler

"""
scales the numeric fesatures of the dataset so that columns with big values such as follower count
and retweet count don't overpower the other features such as verified and mention count.
"""

def scale_features(df):
    feature_cols = [
        'Follower Count',
        'Retweet Count',
        'Mention Count',
        'Verified'
    ]

    scaled_df = df.copy()
    scaler = StandardScaler()
    scaled_df[feature_cols] = scaler.fit_transform(scaled_df[feature_cols])
    return scaled_df, scaler


#creating a sample dataset to test the working of the function
if __name__ == "__main__":
    mock_data = pd.DataFrame({
        'Follower Count': [2353, 9617, 4363, 1204],
        'Retweet Count': [85, 55, 6, 21],
        'Mention Count': [1, 5, 2, 2],
        'Verified': [0, 1, 1, 1]
        })

    scaled, fitted_scaler = scale_features(mock_data)
    print(scaled)