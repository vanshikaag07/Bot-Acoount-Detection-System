"""Generate and validate synthetic tweets for AI4SMA's second 12,500 rows.

Uses local Ollama; never modifies the source CSV. Reuses previous
output_ollama/progress_all.jsonl checkpoints from the original generator.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

START = 12500  # Zero-based index: CSV data row 12,501
END = 25000    # Exclusive: last data row is 25,000
TOPICS = ["college life", "sports", "technology", "music", "local events", "food", "travel", "weather", "gaming", "work", "shopping", "entertainment", "pets", "fitness", "community updates", "books", "public transit", "photography", "movies", "hobbies"]
STYLES = ["casual update", "question", "short announcement", "observation", "recommendation", "reaction", "helpful tip", "event notice", "lighthearted comment", "promotional message"]
MENTIONS = re.compile(r"(?<![\w@])@[A-Za-z0-9_]{1,15}\b")
HASHTAGS = re.compile(r"(?<![\w#])#([A-Za-z0-9_]+)\b")


def call_ollama(model, prompt):
    """Request one JSON response from the locally installed Ollama model."""
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "format": "json", "options": {"temperature": 0.9}}).encode("utf-8")
    request = urllib.request.Request("http://127.0.0.1:11434/api/generate",
                                     data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        body = json.load(response)
    return json.loads(body["response"])


def load_rows(path):
    """Read the original dataset, checking its columns and row count."""
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames
        rows = list(reader)
    needed = {"Tweet", "Bot Label", "Mention Count", "Hashtags"}
    if not fields or not needed.issubset(fields):
        raise ValueError(f"Input CSV must contain: {', '.join(sorted(needed))}")
    if len(rows) != 50000:
        raise ValueError(f"Expected 50,000 data rows; found {len(rows)}. Stop and verify input.")
    return fields, rows


def save_csv(path, fields, rows):
    """Write output to a temporary file first, then replace final file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def normalize_tweet(text):
    """Make whitespace consistent, so every tweet occupies one CSV cell."""
    return " ".join(text.split()).strip()


def metadata_for_tweet(tweet):
    """Count @mentions and extract #hashtags from the new tweet text."""
    count = len(MENTIONS.findall(tweet))
    tags = HASHTAGS.findall(tweet)
    # Kaggle original stores hashtags as space-separated words WITHOUT '#'.
    return str(count), " ".join(dict.fromkeys(tags))


def load_progress(checkpoint, original_sha, rows, eligible):
    """Reuse earlier Ollama generations but reject invalid or mismatched checkpoints."""
    progress = {}
    if not checkpoint.exists():
        return progress
    allowed = set(eligible)
    with checkpoint.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("source_sha256") != original_sha:
                raise ValueError("Checkpoint belongs to a different input CSV. Use a new --output folder.")
            index, tweet = item.get("index"), item.get("tweet")
            if type(index) is not int or index not in allowed or not isinstance(tweet, str):
                raise ValueError(f"Invalid checkpoint at line {line_number}")
            if not 15 <= len(normalize_tweet(tweet)) <= 260:
                raise ValueError(f"Invalid tweet length at checkpoint line {line_number}")
            if index in progress and progress[index] != tweet:
                raise ValueError(f"Conflicting saved tweets for row {index + 1}")
            progress[index] = normalize_tweet(tweet)
    values = [v.casefold() for v in progress.values()]
    if len(values) != len(set(values)):
        raise ValueError("Duplicate tweets in checkpoint; review and fix before resuming")
    return progress


def create_prompt(index, label):
    """Pick a reproducible topic and style for each dataset row."""
    rng = random.Random(index * 1337)
    topic, style = rng.choice(TOPICS), rng.choice(STYLES)
    character = "an automated account" if label == "1" else "a regular person"
    return (f"Create ONE fictional, realistic Twitter/X-style post written by {character}. "
            f"Topic: {topic}. Style: {style}. Be specific and natural; vary length, punctuation and voice. "
            "For automated accounts, sometimes use service updates, promotions, reminders, or engagement prompts, "
            "but do not make every bot obvious. For human accounts, use believable personal details or opinions. "
            "Do not impersonate real people, fabricate urgent safety alerts, or include real URLs. "
            'No preamble. Respond with JSON exactly like {"tweet":"..."}. '
            "The tweet must be 15 to 260 characters, single-line, and avoid generic motivational filler.")


def validate_outputs(original, updated, progress, eligible):
    """Check that only authorized rows and columns were modified."""
    if len(original) != len(updated):
        raise ValueError("Wrong output row count")
    allowed_columns = {"Tweet", "Mention Count", "Hashtags"}
    eligible_set = set(eligible)
    for i, (before, after) in enumerate(zip(original, updated)):
        if i not in eligible_set or i not in progress:
            if before != after:
                raise ValueError(f"Unexpected change to unchanged row {i+1}")
        else:
            for key in before:
                if key not in allowed_columns and before[key] != after[key]:
                    raise ValueError(f"Unexpected change to {key} at row {i+1}")
            if after["Tweet"] != progress[i]:
                raise ValueError(f"Tweet mismatch at row {i+1}")
            mentions, tags = metadata_for_tweet(after["Tweet"])
            if after["Mention Count"] != mentions or after["Hashtags"] != tags:
                raise ValueError(f"Metadata mismatch at row {i+1}")
    print(f"Validation passed: {len(progress)} generated tweet(s), {len(original)} total rows, outside rows unchanged.")


def main():
    parser = argparse.ArgumentParser(description="Rebuild second 12,500 tweets locally using Ollama")
    parser.add_argument("--input", default="bot_detection_data.csv")
    parser.add_argument("--scope", choices=("all", "bots"), default="all")
    parser.add_argument("--count", type=int, default=5, help="Total target completed rows (includes saved progress)")
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--output", default="output_ollama")
    parser.add_argument("--validate-only", action="store_true", help="Rebuild/check saved tweets without calling Ollama")
    args = parser.parse_args()
    if not 1 <= args.count <= 12500:
        parser.error("--count must be between 1 and 12500")

    input_path = Path(args.input)
    fields, rows = load_rows(input_path)
    original_sha = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    checkpoint = output / f"progress_{args.scope}.jsonl"
    eligible = [i for i in range(START, END) if args.scope == "all" or rows[i]["Bot Label"].strip() == "1"]
    progress = load_progress(checkpoint, original_sha, rows, eligible)
    seen = {tweet.casefold() for tweet in progress.values()}
    selected = eligible[:args.count]

    if not args.validate_only:
        for i in selected:
            if i in progress:
                continue
            label = rows[i]["Bot Label"].strip()
            if label not in ("0", "1"):
                raise ValueError(f"Unexpected Bot Label {label!r} at CSV row {i+1}")
            prompt = create_prompt(i, label)
            for attempt in range(3):
                try:
                    reply = call_ollama(args.model, prompt)
                    tweet = normalize_tweet(reply["tweet"])
                    if not 15 <= len(tweet) <= 260 or tweet.casefold() in seen:
                        raise ValueError("Tweet length invalid or duplicate")
                    break
                except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
                    if attempt == 2:
                        raise RuntimeError(f"Failed at CSV row {i+1}: {exc}") from exc
                    time.sleep(2)
            progress[i] = tweet
            seen.add(tweet.casefold())
            with checkpoint.open("a", encoding="utf-8") as saved:
                saved.write(json.dumps({"source_sha256": original_sha, "index": i, "tweet": tweet}, ensure_ascii=False) + "\n")
            print(f"Generated {sum(k in progress for k in selected)}/{len(selected)}: CSV row {i+1} — {tweet[:65]}", flush=True)

    full = [dict(row) for row in rows]
    for i in eligible:
        if i in progress:
            tweet = progress[i]
            mentions, hashtags = metadata_for_tweet(tweet)
            full[i]["Tweet"] = tweet
            full[i]["Mention Count"] = mentions
            full[i]["Hashtags"] = hashtags
    validate_outputs(rows, full, progress, eligible)
    save_csv(output / "second_12500_section.csv", fields, full[START:END])
    save_csv(output / "full_50000_rebuilt.csv", fields, full)
    audit_path = output / "audit.csv"
    with audit_path.open("w", encoding="utf-8", newline="") as audit:
        writer = csv.writer(audit)
        writer.writerow(["CSV row (excluding header)", "Bot Label", "Original Tweet", "New Tweet", "New Mention Count", "New Hashtags"])
        for i in eligible:
            if i in progress:
                writer.writerow([i+1, rows[i]["Bot Label"], rows[i]["Tweet"], progress[i], full[i]["Mention Count"], full[i]["Hashtags"]])
    print(f"Done: {len(progress)} of {len(eligible)} eligible rows generated. Files saved in {output}/")
    print("NOTE: Retweet Count and other account metadata remain original; review for modeling consistency.")
    print("NOTE: Synthetic-text labels and validation/test leakage risks must be reviewed before model training.")


if __name__ == "__main__":
    main()
