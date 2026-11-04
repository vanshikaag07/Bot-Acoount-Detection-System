"""Generate synthetic tweet text with local Ollama for assigned CSV rows.

Never edits the input CSV. Test with --count 5 before a full run.
"""
import argparse
import csv
import hashlib
import json
import random
import time
import urllib.error
import urllib.request
from pathlib import Path

TOPICS = ["college life", "sports", "technology", "music", "local events", "food", "travel", "weather", "gaming", "work", "shopping", "entertainment", "pets", "fitness", "community updates", "books", "public transit", "photography", "movies", "hobbies"]
STYLES = ["casual update", "question", "short announcement", "observation", "recommendation", "reaction", "helpful tip", "event notice", "lighthearted comment", "promotional message"]


def call_ollama(model, prompt):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "format": "json", "options": {"temperature": 0.9}}).encode("utf-8")
    request = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        body = json.load(response)
    return json.loads(body["response"])


def load_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames
        rows = list(reader)
    if not fields or not {"Tweet", "Bot Label"}.issubset(fields):
        raise ValueError("Input CSV must contain Tweet and Bot Label columns")
    if len(rows) < 25000:
        raise ValueError("Input dataset has fewer than 25,000 rows")
    return fields, rows


def save_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Rebuild second 12,500 tweets locally using Ollama")
    parser.add_argument("--input", default="bot_detection_data.csv")
    parser.add_argument("--scope", choices=("all", "bots"), default="all")
    parser.add_argument("--count", type=int, default=5, help="Maximum rows to generate this run, default 5")
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--output", default="output_ollama")
    args = parser.parse_args()
    if args.count < 1 or args.count > 12500:
        parser.error("--count must be between 1 and 12500")
    fields, rows = load_rows(Path(args.input))
    original_sha = hashlib.sha256(Path(args.input).read_bytes()).hexdigest()
    output = Path(args.output)
    output.mkdir(exist_ok=True, parents=True)
    checkpoint = output / f"progress_{args.scope}.jsonl"
    progress = {}
    if checkpoint.exists():
        with checkpoint.open(encoding="utf-8") as source:
            for line in source:
                item = json.loads(line)
                if item.get("source_sha256") != original_sha:
                    raise ValueError("Checkpoint belongs to a different input CSV. Use a new --output folder.")
                progress[item["index"]] = item["tweet"]
    eligible = [i for i in range(12500, 25000) if args.scope == "all" or rows[i]["Bot Label"].strip() == "1"]
    seen = set(t.casefold().strip() for t in progress.values())
    selected = eligible[:args.count]
    for i in selected:
        if i in progress:
            continue
        label = rows[i]["Bot Label"].strip()
        if label not in ("0", "1"):
            raise ValueError(f"Unexpected Bot Label {label!r} at row {i+1}")
        rng = random.Random(i * 1337)
        topic = rng.choice(TOPICS)
        style = rng.choice(STYLES)
        character = "an automated account" if label == "1" else "a regular person"
        prompt = (f"Create ONE fictional, realistic Twitter/X-style post written by {character}. "
                  f"Topic: {topic}. Style: {style}. Be specific and natural; vary length, punctuation and voice. "
                  "For automated accounts, sometimes use service updates, promotions, reminders, or engagement prompts, "
                  "but do not make every bot obvious. For human accounts, use believable personal details or opinions. "
                  "Do not impersonate real people, fabricate urgent safety alerts, or include real URLs. "
                  "No preamble. Respond with JSON exactly like {\"tweet\":\"...\"}. "
                  "The tweet must be 15 to 260 characters, single-line, and avoid generic motivational filler.")
        for attempt in range(3):
            try:
                reply = call_ollama(args.model, prompt)
                tweet = reply["tweet"].replace("\n", " ").strip()
                if not 15 <= len(tweet) <= 260 or tweet.casefold() in seen:
                    raise ValueError("Tweet length invalid or duplicate")
                break
            except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
                if attempt == 2:
                    raise RuntimeError(f"Failed at CSV row {i+1}: {exc}") from exc
                time.sleep(2)
        progress[i] = tweet
        seen.add(tweet.casefold())
        with checkpoint.open("a", encoding="utf-8") as out:
            out.write(json.dumps({"source_sha256": original_sha, "index": i, "tweet": tweet}, ensure_ascii=False) + "\n")
        print(f"Generated {len([k for k in selected if k in progress])}/{len(selected)}: CSV row {i+1} — {tweet[:65]}", flush=True)
    replacement = [dict(row) for row in rows[12500:25000]]
    full = [dict(row) for row in rows]
    for i in eligible:
        if i in progress:
            full[i]["Tweet"] = progress[i]
            replacement[i - 12500]["Tweet"] = progress[i]
    save_csv(output / "second_12500_section.csv", fields, replacement)
    save_csv(output / "full_50000_rebuilt.csv", fields, full)
    with (output / "audit.csv").open("w", encoding="utf-8", newline="") as audit:
        writer = csv.writer(audit)
        writer.writerow(["CSV row (excluding header)", "Bot Label", "Original Tweet", "New Tweet"])
        for i in eligible:
            if i in progress:
                writer.writerow([i+1, rows[i]["Bot Label"], rows[i]["Tweet"], progress[i]])
    print(f"Done: {len([i for i in eligible if i in progress])} of {len(eligible)} eligible rows generated. Files saved in {output}/")
    print("NOTE: Count/hashtags metadata are unchanged and may not match the new text. Review before training.")


if __name__ == "__main__":
    main()
