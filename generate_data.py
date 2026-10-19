# Gemini AI was used to help me code this script.

import os
import time
import pandas as pd
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# 1. Base directory setup
BASE_DIR = Path(__file__).resolve().parent

# Force load_dotenv to look in the exact directory of this script
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(f"API key not found at {env_path}! Check that GEMINI_API_KEY is set in your .env file.")

client = genai.Client(api_key=api_key)

# 2. File paths
input_file = BASE_DIR / "bot_detection_data.csv"
output_file = BASE_DIR / "bot_detection_data_updated.csv"

if not input_file.exists():
    raise FileNotFoundError(f"Could not find '{input_file.name}' in {BASE_DIR}.")

df = pd.read_csv(input_file)

# Take the first 1000 rows
df_subset = df.head(1000).copy()

# System prompts tailored to each label
HUMAN_PROMPT = "Write a single realistic human tweet. Use natural, casual language, minor typos or informal phrasing, personal opinions, or everyday commentary. Do not include hashtags unless natural. Maximum 280 characters."
BOT_PROMPT = "Write a single realistic Twitter bot tweet. Use structured, repetitive, or promotional language, frequent links/hashtags, automated news/crypto/deal updates, or spammy phrasings. Maximum 280 characters."

def generate_tweet(label):
    prompt = BOT_PROMPT if label == 1 else HUMAN_PROMPT
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        return response.text.strip().strip('"')
    except Exception as e:
        print(f"\nError generating tweet: {e}")
        time.sleep(2)
        return None

# 3. Target columns from your dataset
text_col = "Tweet"
label_col = "Bot Label"

new_tweets = []
human_previews = []
bot_previews = []

print("Processing 1,000 tweets in background...\n")

for index, row in df_subset.iterrows():
    original_tweet = row[text_col]
    label = row[label_col]  # 1 = Bot, 0 = Human
    
    new_tweet = generate_tweet(label)
    new_tweets.append(new_tweet)
    
    # Store first 5 human and first 5 bot replacements for display
    if label == 0 and len(human_previews) < 5:
        human_previews.append((index + 1, original_tweet, new_tweet))
    elif label == 1 and len(bot_previews) < 5:
        bot_previews.append((index + 1, original_tweet, new_tweet))

# 4. Save updated dataframe
df_subset[text_col] = new_tweets
df_subset.to_csv(output_file, index=False)

# 5. Display sample preview
print("=" * 60)
print("           SAMPLE PREVIEW (5 HUMAN & 5 BOT)           ")
print("=" * 60)

print("\n--- 5 HUMAN TWEETS ---")
for row_num, orig, new_t in human_previews:
    print(f"Row {row_num} [HUMAN]:")
    print(f"  ORIGINAL: {orig}")
    print(f"  REPLACED: {new_t}\n")

print("--- 5 BOT TWEETS ---")
for row_num, orig, new_t in bot_previews:
    print(f"Row {row_num} [BOT]:")
    print(f"  ORIGINAL: {orig}")
    print(f"  REPLACED: {new_t}\n")

print("=" * 60)
print(f"Done! Updated 'Tweet' column for 1,000 rows and saved to '{output_file.name}'")