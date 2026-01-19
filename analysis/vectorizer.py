from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_features(texts):
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        stop_words="english"
    )
    X = vectorizer.fit_transform(texts)
    return X
