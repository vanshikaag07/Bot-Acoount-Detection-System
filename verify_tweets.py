import pandas as pd

g = pd.read_csv("generated_tweets.csv")
r = pd.read_csv("rows_to_fill.csv").head(1000)

print("rows:", len(g))
print("row_index matches:", (g["row_index"].values == r["row_index"].values).all())
print("labels match:", (g["Bot Label"].values == r["Bot Label"].values).all())
print("tweets unique:", g["Tweet"].is_unique, "| blanks:", g["Tweet"].isna().sum())
print(g["Bot Label"].value_counts())
print(g.sample(20, random_state=1)[["Bot Label", "Tweet"]].to_string())