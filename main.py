from scraper.twitter_scraper import TwitterScraper
import pandas as pd
import time

from processing.cleaner import clean
from processing.deduplicator import deduplicate
from storage.parquet_store import save

from analysis.vectorizer import tfidf_features
from analysis.signal_builder import build_signal
from analysis.visualization import plot_signal

HASHTAGS = ["nifty50", "sensex", "banknifty", "intraday"]

def scrape_sequential():
    scraper = TwitterScraper()
    all_tweets = []

    try:
        for tag in HASHTAGS:
            print(f"Scraping #{tag} ...")
            tweets = scraper.scrape_hashtag(tag, max_tweets=500)
            all_tweets.extend(tweets)
            print(f"tweets len for #{tag} ..."+str(len(tweets)))
            time.sleep(10)

    finally:
        scraper.close()

    return all_tweets


def preprocess(tweets):
    for t in tweets:
        t["content"] = clean(t["content"])
    return deduplicate(tweets)

def run_analysis(parquet_path):
    df = pd.read_parquet(parquet_path)

    texts = df["content"].tolist()

    # Vectorization
    X = tfidf_features(texts)
    # Signal computation
    strength, confidence = build_signal(X)
    #print(strength)
    print(f"Generated {len(strength)} sentiment signals")

    # Visualization (sampled)
    plot_signal(strength)


if __name__ == "__main__":
    print("Starting market intelligence pipeline...")

    tweets = scrape_sequential()
    print(f"Scraped {len(tweets)} raw tweets")

    tweets = preprocess(tweets)
    print(f"{len(tweets)} tweets after cleaning & deduplication")

    parquet_path = "data/processed/tweets.parquet"
    save(tweets, parquet_path)
    print("Data saved to Parquet")

    run_analysis(parquet_path)
