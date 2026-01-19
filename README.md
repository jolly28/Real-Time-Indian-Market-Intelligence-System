# Real-Time-Indian-Market-Intelligence-System
A production-ready data collection and analysis system for extracting real-time market intelligence from Twitter/X discussions related to the Indian stock market.
This project demonstrates web scraping without paid APIs, scalable data processing, efficient storage, and text-to-signal transformation suitable for algorithmic trading research.

### Key Features
#### ✅ Data Collection (No Paid APIs)
- Selenium-based scraping (Twitter/X web)
- Human-like scrolling and randomized delays
- Multiple hashtag scraping: #nifty50, #sensex, #banknifty, #intraday
- Collects 2000+ tweets from the last 24-48 hours

#### ✅ Data Processing
- Text cleaning and normalization
- Hash-based deduplication

#### ✅ Efficient Storage
- Columnar Parquet format
- Memory-efficient and analytics-ready
- Suitable for large-scale time-series analysis

#### ✅ Text → Trading Signal Conversion
- TF-IDF vectorization (unigrams + bigrams)
- Composite signal generation: Signal strength and Confidence estimation

### TO-DO
Concurrent scraping using thread pools (handling multiple chrome profile twitter login)

### Running the Pipeline
```
pip install -r requirements.txt
python main.py
```


main.py will:
- Scrape tweets from multiple Indian market hashtags
- Clean & deduplicate data
- Store results in data/processed/tweets.parquet
- Generate quantitative sentiment signals
- Display memory-efficient visualizations

IDE: PyCharm
Python: 3.13
