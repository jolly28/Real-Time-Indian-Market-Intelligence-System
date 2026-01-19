def build_signal(X):
    dense_X = X.toarray()  # convert sparse to dense
    strength = dense_X.mean(axis=1)  # mean across features
    confidence = dense_X.std(axis=1)  # std across features
    return strength, confidence
