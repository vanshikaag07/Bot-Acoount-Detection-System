import pandas as pd
from split_data import split_data

# simple unit test to ensure dataset splitting works properly
def test_split_data():
    # generate dummy mock dataset with 100 rows and balanced target labels
    df = pd.DataFrame({
        'feature1': range(100),
        'feature2': range(100),
        'Bot Label': [0, 1] * 50
    })
    
    # run the split function 70 percent train 15 percent val 15 percent test
    train, val, test = split_data(df)
    
    # quick sanity check total row count across all splits should equal original input
    assert len(train) + len(val) + len(test) == 100
    
    # verify class distribution remains approximately 50 50 in each subset
    for split in [train, val, test]:
        ratio = split['Bot Label'].value_counts(normalize=True)
        assert abs(ratio[0] - 0.5) < 0.1
        assert abs(ratio[1] - 0.5) < 0.1
