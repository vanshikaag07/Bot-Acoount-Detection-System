'''This script was writen by Claude AI to generate Kavin's share of the 12500 tweets in bot_detection_data.csv.'''

"""Replace the Tweet column for the last 12,500 rows (Kavin's share) with locally
generated bot-style / human-style text. No external APIs: all phrase pools are
hand-written below and combined randomly (seeded for reproducibility).

Usage: python generate_kavin_share.py
Reads bot_detection_data.csv, writes bot_detection_data_kavin_share.csv.
"""

import random
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent
SRC = PROJECT / "bot_detection_data.csv"
DST = PROJECT / "bot_detection_data_kavin_share.csv"
SHARE = 12_500
BATCH = 2_500

rng = random.Random(42)
pick = rng.choice

# ----------------------------------------------------------------- bot pools
COINS = ["$BTC", "$ETH", "$SOL", "$DOGE", "$PEPE", "$XRP", "$SHIB", "$BNB", "$ADA",
         "$AVAX", "$LINK", "$MATIC", "$ARB", "$WIF", "$BONK", "$TON", "$SUI", "$INJ"]
GAINS = ["10x", "50x", "100x", "1000x", "20x", "5x", "300%", "500%", "800%", "1200%"]
MOON_EMOJI = ["🚀", "🚀🚀🚀", "🔥", "🔥🔥", "💎🙌", "🌕", "📈", "💰", "🤑", "⚡️", "✅", "👇", "💯", "🎁"]
CTA = ["Don't miss out!", "Act fast!", "Last chance!", "Limited spots left!", "Only 24 hours left!",
       "DM me now!", "Link in bio!", "Click the link below!", "Join now before it's too late!",
       "Spots filling up FAST!", "Hurry!!", "Get in early!", "Tap the link 👇", "Claim yours now!",
       "Offer ends tonight!", "This won't last!", "Turn on notifications!"]
LINKS = ["bit.ly/{c}", "tinyurl.com/{c}", "t.co/{c}", "cutt.ly/{c}", "rb.gy/{c}", "shorturl.at/{c}",
         "is.gd/{c}", "linktr.ee/{c}"]
CRYPTO_TAGS = ["#crypto", "#Bitcoin", "#BTC", "#ETH", "#altcoins", "#altseason", "#memecoin",
               "#100x", "#Web3", "#NFT", "#DeFi", "#airdrop", "#cryptonews", "#bullrun",
               "#HODL", "#blockchain", "#presale", "#gem"]
POL_TAGS = ["#WakeUp", "#TruthMatters", "#Patriots", "#Resist", "#StandUp", "#SpreadTheWord",
            "#Breaking", "#Freedom", "#WeThePeople", "#Corruption", "#Election", "#Exposed",
            "#ShareThis", "#Retweet", "#News"]
PROMO_TAGS = ["#giveaway", "#free", "#deal", "#sale", "#discount", "#win", "#contest",
              "#followback", "#F4F", "#gain", "#promo", "#ad", "#sponsored", "#shopping",
              "#makemoneyonline", "#sidehustle", "#passiveincome"]
ENGAGE_TAGS = ["#followback", "#F4F", "#teamfollowback", "#gainwithxtiandela", "#followtrain",
               "#RT", "#likeforlike", "#L4L", "#follow4follow", "#trending"]
PRODUCTS = ["wireless earbuds", "smart watch", "iPhone 16", "PS5", "gaming laptop", "AirPods",
            "$500 gift card", "$1000 Amazon card", "Apple Watch", "Nintendo Switch", "designer bag",
            "$250 Visa card", "MacBook", "robot vacuum", "skincare bundle", "LED strip lights",
            "posture corrector", "phone case", "massage gun", "air fryer"]
DISCOUNTS = ["50% OFF", "70% OFF", "80% OFF", "BUY 1 GET 1 FREE", "90% OFF", "FREE SHIPPING",
             "60% OFF", "FLASH SALE", "CLEARANCE", "40% OFF TODAY ONLY"]
POL_TOPICS = ["the election", "the economy", "the media", "the government", "Big Tech",
              "the border", "the banks", "the elites", "Congress", "the mainstream media",
              "the deep state", "the courts", "Washington", "the system", "the polls",
              "inflation", "the WHO", "the Fed", "the establishment"]
POL_VERBS = ["is hiding", "doesn't want you to know", "is lying about", "is covering up",
             "won't report", "is censoring", "just got exposed for", "is panicking about",
             "is terrified of"]
POL_OBJECTS = ["the truth", "what really happened", "the real numbers", "this story",
               "the facts", "what's coming next", "the evidence", "the documents"]
MOTIVATION = ["Success is a mindset.", "Your vibe attracts your tribe.", "Grind now, shine later.",
              "Rich people think differently.", "Stop waiting. Start doing.",
              "Winners never quit.", "Dream big, work hard.", "Your network is your net worth.",
              "Hustle in silence.", "Make money while you sleep.", "Mindset is everything.",
              "Discipline beats motivation.", "Be the energy you want to attract.",
              "The 9-5 is a trap.", "Invest in yourself."]
NUMS = ["1000", "5000", "10K", "50K", "2,500", "100", "500", "20K"]
NEWS_HEAD = ["BREAKING", "JUST IN", "ALERT", "URGENT", "🚨 BREAKING 🚨", "⚠️ WARNING",
             "🔴 LIVE", "HUGE NEWS", "DEVELOPING"]

BOT_TEMPLATES = [
    "{coin} is about to EXPLODE {e} {gain} incoming! {cta} {link} {ct} {ct2}",
    "{coin} just broke resistance {e} Next stop {gain}. Not financial advice but... {ct} {ct2}",
    "Why is nobody talking about {coin}?? {gain} gem hiding in plain sight {e} {ct}",
    "🚨 {coin} PRESALE LIVE 🚨 {gain} potential. {cta} {link} {ct} {ct2} {ct3}",
    "I turned $500 into ${amt} with {coin} in {days} days {e} Want to know how? DM me {ct}",
    "Massive {coin} airdrop happening NOW {e} Connect wallet to claim: {link} {ct} {ct2}",
    "{coin} whales are accumulating 🐋 {gain} is coming. Load your bags {e} {ct}",
    "If you're not holding {coin} right now you're going to regret it {e} {ct} {ct2}",
    "Bull run confirmed {e} {coin} {coin2} {coin3} all ready to send {ct} {ct2}",
    "Top 3 coins to {gain} this month: {coin} {coin2} {coin3} {e} RT if you're holding {ct}",
    "{head}: {topic} {pverb} {pobj}. RT before they delete this! {pt} {pt2}",
    "{head} — {topic} {pverb} {pobj}!!! Share everywhere {e} {pt}",
    "They don't want you to see this. {topic} {pverb} {pobj}. {pt} {pt2} {pt3}",
    "Wake up people! {topic} {pverb} {pobj}. Retweet if you agree {pt}",
    "Retweet if you think {topic} {pverb} {pobj} 🇺🇸 {pt} {pt2}",
    "The truth about {topic} is finally coming out {e} Follow for more {pt} {pt2}",
    "{pct}% of people don't know that {topic} {pverb} {pobj}. Spread the word {pt}",
    "🎁 GIVEAWAY 🎁 Win a {product}! To enter: 1. Follow 2. RT 3. Tag 3 friends {ct_p} {ct_p2}",
    "We're giving away a {product} to one lucky follower {e} Follow + RT to enter! Ends {when} {ct_p}",
    "{disc} on {product} {e} {cta} {link} {ct_p} {ct_p2}",
    "🔥 {disc} 🔥 {product} — {cta} {link} {ct_p}",
    "Hot deal alert! {product} now {disc} {e} Shop now: {link} {ct_p} {ct_p2}",
    "Get your {product} before they sell out!! {disc} {e} {link}",
    "Earn ${amt}/week from home with this one simple trick {e} {cta} {link} {ct_p}",
    "I made ${amt} last month working from my phone. {cta} {link} {ct_p} {ct_p2}",
    "Want {num} followers FAST? {cta} {link} {ct_e}",
    "Follow me and I'll follow back 100% {e} {ct_e} {ct_e2} {ct_e3}",
    "Like if you agree, RT if you strongly agree {e} {ct_e}",
    "Who's still awake? Drop a {e1} below 👇 {ct_e}",
    "Retweet this if you want more followers! Everyone who RTs gets a follow {e} {ct_e} {ct_e2}",
    "Comment YES if you want to {goal} in 2026 {e} {ct_e}",
    "Follow everyone who likes this {e} {ct_e} {ct_e2}",
    "{motive} {e} {ct_m}",
    "{motive} {motive2} {e} Follow for daily motivation {ct_m}",
    "{motive} Agree? 👇 {ct_m} {ct_m2}",
    "Good morning everyone! {motive} Have a blessed day {e} {ct_e}",
    "Tag someone who needs to hear this: {motive} {e}",
    "Check out this amazing opportunity!!! {e} {link}",
    "Click here for exclusive content {e} {link} {ct_p}",
    "Thank you for following! Check out my page {link} {e}",
    "New post is up! {link} {e} {ct_e}",
    "Trending now: {coin} {e} {link} {ct}",
    "Daily reminder: {motive} {link}",
    "Congratulations! You have been selected to receive a {product}. Claim here: {link}",
    "Your account has been selected for a reward {e} Verify now: {link}",
    "{num} people already joined. Will you be next? {cta} {link} {ct_p}",
    "Just dropped: {product} at {disc} {e} {ct_p} {link}",
    "Amazing content! Follow for more {e} {ct_e} {ct_e2}",
    "Great post! Check out my profile for more {e} {link}",
]
GOALS = ["make money online", "quit your 9-5", "become financially free", "grow your account",
         "get rich", "retire early", "start a business", "go viral"]
WHEN = ["Friday", "tonight", "in 24 hours", "Sunday", "at midnight", "this weekend", "soon"]


def link():
    code = "".join(rng.choice("abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                   for _ in range(rng.randint(5, 8)))
    return "https://" + pick(LINKS).format(c=code)


def bot_tweet():
    coins = rng.sample(COINS, 3)
    vals = dict(
        coin=coins[0], coin2=coins[1], coin3=coins[2], gain=pick(GAINS), e=pick(MOON_EMOJI),
        e1=pick(["❤️", "🔥", "🙌", "💯", "👍", "😂"]), cta=pick(CTA), link=link(),
        ct=pick(CRYPTO_TAGS), ct2=pick(CRYPTO_TAGS), ct3=pick(CRYPTO_TAGS),
        pt=pick(POL_TAGS), pt2=pick(POL_TAGS), pt3=pick(POL_TAGS),
        ct_p=pick(PROMO_TAGS), ct_p2=pick(PROMO_TAGS),
        ct_e=pick(ENGAGE_TAGS), ct_e2=pick(ENGAGE_TAGS), ct_e3=pick(ENGAGE_TAGS),
        ct_m=pick(["#motivation", "#success", "#mindset", "#hustle", "#entrepreneur", "#goals"]),
        ct_m2=pick(["#grind", "#inspiration", "#wealth", "#bossmindset", "#money"]),
        head=pick(NEWS_HEAD), topic=pick(POL_TOPICS), pverb=pick(POL_VERBS), pobj=pick(POL_OBJECTS),
        product=pick(PRODUCTS), disc=pick(DISCOUNTS), amt=f"{rng.randint(2, 60) * 500:,}",
        days=rng.choice([3, 5, 7, 10, 14, 30]), num=pick(NUMS), pct=rng.choice([90, 95, 97, 99, 80]),
        motive=pick(MOTIVATION), motive2=pick(MOTIVATION), goal=pick(GOALS), when=pick(WHEN),
    )
    t = pick(BOT_TEMPLATES).format(**vals)
    if rng.random() < 0.15:
        t = t.upper()
    return " ".join(t.split())


# --------------------------------------------------------------- human pools
FOODS = ["tacos", "leftover pad thai", "a bagel", "cold pizza", "ramen", "a burrito the size of my head",
         "my mom's biryani", "chicken nuggets", "pho", "grilled cheese", "a sad desk salad",
         "pancakes", "dumplings", "mac and cheese", "a gas station hot dog", "sushi", "cereal for dinner",
         "chili", "an entire bag of goldfish", "butter chicken", "a Chick-fil-A sandwich", "pasta"]
PLACES = ["the library", "Target", "the DMV", "the gym", "Costco", "work", "the dentist",
          "my cousin's wedding", "the airport", "class", "the laundromat", "Trader Joe's",
          "the coffee shop", "my apartment", "the parking garage", "the farmers market",
          "Walmart at 11pm", "the vet", "my sister's place", "the train station", "lab"]
PEOPLE = ["my roommate", "my mom", "my dad", "my coworker", "my sister", "my brother",
          "my best friend", "my boyfriend", "my girlfriend", "my neighbor", "my professor",
          "my boss", "my grandma", "the barista", "my lab partner", "my cat", "my dog",
          "my 4 year old nephew", "my partner", "a guy on the bus"]
SHOWS = ["Severance", "The Bear", "Succession", "the new Dune", "Bluey", "Love Island",
         "The Office for the 9th time", "Breaking Bad", "the Taylor Swift doc", "Arcane",
         "that new Netflix true crime thing", "the Oppenheimer rewatch", "Shrinking", "Abbott Elementary",
         "The Last of Us", "Great British Bake Off", "Survivor"]
TEAMS = ["the Colts", "the Pacers", "Purdue", "the Bears", "the Cubs", "the Lakers",
         "the Packers", "the Yankees", "Arsenal", "the Celtics", "the Chiefs", "IU"]
TIMES = ["at 2am", "this morning", "last night", "today", "on my lunch break", "this weekend",
         "at 6am", "before work", "after class", "on a Tuesday", "for the third time this week",
         "yesterday", "right now"]
FEELINGS = ["lowkey proud of myself", "so tired", "kind of emotional about it", "weirdly happy",
            "honestly fine with it", "not okay", "thriving", "running on 4 hours of sleep",
            "too old for this", "in my feelings", "exhausted but happy", "mildly annoyed"]
ACTIVITIES = ["finished my first 5k", "fixed the sink myself", "finally cleaned my car",
              "beat my sourdough curse", "passed my driving test", "submitted the assignment with 2 minutes left",
              "assembled an IKEA dresser without crying", "ran into my high school teacher",
              "locked myself out of my apartment", "spilled coffee on my only clean shirt",
              "accidentally replied all to the whole department", "parallel parked on the first try",
              "got a parking ticket", "missed the bus by literally 3 seconds", "repotted all my plants",
              "finished a book for the first time in months", "deep cleaned the fridge",
              "dyed my hair", "learned how to change a tire", "did a whole grocery run without forgetting anything",
              "fell asleep on the couch at 8pm", "went on a 10 mile bike ride",
              "burned the rice somehow", "set off the smoke alarm making toast"]
WEATHER = ["it's 40 degrees and raining", "it's somehow 85 in October", "it snowed in April",
           "the wind almost took my umbrella", "the sunset tonight was unreal", "it's so humid I can't breathe",
           "the first cold morning of the year finally hit", "it's been gray for 9 days straight"]
REACTIONS = ["lol", "lmao", "😭", "🙃", "ugh", "honestly", "smh", "😂", "🥲", "idk", "help", "", "", "", ""]

HUMAN_TEMPLATES = [
    "just {activity} {time} and I'm {feeling}",
    "{time} I {activity}. {reaction}",
    "{person} just told me I've been saying it wrong my whole life {reaction}",
    "had {food} {time} and it slapped",
    "eating {food} {time} because I refuse to cook",
    "why does {place} always have exactly one line open",
    "went to {place} for one thing and left with 14 things {reaction}",
    "{person} keeps stealing my hoodies and at this point I've accepted it",
    "{person} called {time} just to tell me about their fantasy league. love them",
    "finally started watching {show} and I get the hype now",
    "no spoilers but the ending of {show} wrecked me",
    "rewatching {show} instead of doing literally anything productive",
    "{team} really said not today huh. I need a minute",
    "can't believe {team} pulled that off. screaming",
    "watching {team} is bad for my blood pressure",
    "{weather} and I am {feeling}",
    "{weather}. this state is not real",
    "does anyone else get weirdly nervous calling to make a dentist appointment or just me",
    "my cat knocked a glass off the counter while maintaining eye contact {reaction}",
    "my dog heard the cheese drawer open from two rooms away. impressive honestly",
    "three hours into this lab report and I've written one paragraph {reaction}",
    "midterms week and I'm surviving on {food} and spite",
    "someone at {place} complimented my jacket and now I'm in a good mood for the whole day",
    "got carded buying cough syrup at 27. thank you I guess",
    "how is it already {month}. where did {prevmonth} go",
    "happy birthday to {person}, the only one who laughs at my bad jokes",
    "{person} made {food} for everyone {time} and I think I'm crying",
    "running late to {place} again. at least I have my coffee",
    "my landlord finally fixed the heater after 3 weeks. small wins",
    "i should be asleep but here we are",
    "the wifi in {place} is held together by hopes and prayers",
    "took a nap at 3pm and woke up at 7pm with no idea what year it is",
    "not me spending $40 at {place} on snacks",
    "{person} and I have been arguing about whether a hot dog is a sandwich for 45 minutes",
    "tried to be healthy and meal prep. ate {food} instead",
    "anyone have a good recommendation for {thing}? mine finally died",
    "officially {age} today. feel exactly the same tbh",
    "my plant that I thought was dead just grew a new leaf. we're so back",
    "can't stop thinking about {food} from that place near {place}",
    "the guy next to me at {place} is on speakerphone and I know way too much about his divorce now",
    "first day at the new job tomorrow. nervous but excited",
    "booked flights home for thanksgiving. {person} is going to cry",
    "accidentally sent a voice memo of me chewing to the group chat {reaction}",
    "{person} said I look tired. I am tired. thanks",
    "made it to {place} in the rain without my umbrella. we move",
    "there is nothing better than clean sheets after a long week",
    "low battery, no charger, 40 minutes from home. pray for me",
    "the barista remembered my order and I feel like a regular in a sitcom",
    "ok {show} season finale tonight who's watching",
    "I've listened to the same song 30 times today and I'm not stopping",
    "found $20 in my winter coat pocket. best day of the year",
]
THINGS = ["headphones", "a laptop bag", "running shoes", "a coffee maker", "a desk chair",
          "a rain jacket", "a phone charger that doesn't break in a week", "noise cancelling earbuds",
          "a backpack", "a mattress", "a vacuum"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def human_tweet():
    m = rng.randrange(12)
    vals = dict(
        activity=pick(ACTIVITIES), time=pick(TIMES), feeling=pick(FEELINGS), reaction=pick(REACTIONS),
        person=pick(PEOPLE), food=pick(FOODS), place=pick(PLACES), show=pick(SHOWS), team=pick(TEAMS),
        weather=pick(WEATHER), month=MONTHS[m], prevmonth=MONTHS[m - 1], thing=pick(THINGS),
        age=rng.randint(19, 45),
    )
    t = " ".join(pick(HUMAN_TEMPLATES).format(**vals).split())
    # sentence-start capitalization varies by person
    if rng.random() < 0.45:
        t = t[0].upper() + t[1:]
    # occasional trailing reaction / emoji
    if rng.random() < 0.15:
        t += " " + pick(["😭", "😂", "🙃", "💀", "🥲", "❤️", "lol", "lmao"])
    # occasional typo: swap two adjacent letters inside a word
    if rng.random() < 0.08:
        words = t.split()
        i = rng.randrange(len(words))
        w = words[i]
        if len(w) > 4 and w.isalpha():
            j = rng.randrange(1, len(w) - 2)
            words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
            t = " ".join(words)
    return t


# --------------------------------------------------------------------- main
df = pd.read_csv(SRC)
start = len(df) - SHARE
share_idx = df.index[start:]
print(f"Loaded {len(df):,} rows. Replacing Tweet for rows {start:,}–{len(df) - 1:,} ({SHARE:,} rows)\n")

seen = set()


def unique(gen):
    for _ in range(50):
        t = gen()
        if t not in seen:
            seen.add(t)
            return t
    return t  # give up on uniqueness after 50 tries (rare)


for b, lo in enumerate(range(0, SHARE, BATCH), 1):
    idx = share_idx[lo:lo + BATCH]
    labels = df.loc[idx, "Bot Label"]
    df.loc[idx, "Tweet"] = [unique(bot_tweet) if l == 1 else unique(human_tweet) for l in labels]
    n_bot = int((labels == 1).sum())
    print(f"Batch {b}/{SHARE // BATCH}: rows {idx[0]:,}–{idx[-1]:,} done "
          f"({n_bot} bot, {len(idx) - n_bot} human) — {lo + len(idx):,}/{SHARE:,}")
    for l in (1, 0):
        r = df.loc[idx][labels == l].iloc[0]
        print(f"   [{'BOT  ' if l else 'HUMAN'}] {r['Tweet']}")
    print()

df.to_csv(DST, index=False)
print(f"Saved {DST.name}")
print(f"Unique tweets in share: {df.loc[share_idx, 'Tweet'].nunique():,}/{SHARE:,}")
