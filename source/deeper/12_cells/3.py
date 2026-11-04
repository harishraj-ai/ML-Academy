from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import ComplementNB

# A text pipeline: words and word pairs, TF-IDF weighting, then naive Bayes
pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), ComplementNB(alpha=0.5)).fit(texts, labels)
for msg in ["claim your cash now", "report for the monday meeting"]:
    print(f"{msg!r:34} -> {'spam' if pipe.predict([msg])[0] else 'ham'}")
print("number of features (words and word pairs):", len(pipe[0].get_feature_names_out()))
