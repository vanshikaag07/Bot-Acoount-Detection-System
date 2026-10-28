import pandas as pd

CSV_PATH = "data/bot_detection_data.csv"  # same file name you used before
N_ROWS = 2000  # tonight: 1000. Full chunk later: 12500

df = pd.read_csv(CSV_PATH)
print("Total rows:", len(df))
print("User ID unique:", df["User ID"].is_unique)

# my chunk = the first N rows of the file (we're replacing existing text)
my_rows = df.head(N_ROWS)

bots = my_rows[my_rows["Bot Label"] == 1]
humans = my_rows[my_rows["Bot Label"] == 0]
print("Bots:", len(bots), "| Humans:", len(humans))

my_rows[["User ID", "Bot Label"]].to_csv(
    "rows_to_fill.csv", index=True, index_label="row_index"
)
print("Saved", len(my_rows), "rows to rows_to_fill.csv")