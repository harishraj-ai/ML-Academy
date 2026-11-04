import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = ["win cash prize now", "cheap meds win big", "claim your free prize", "free cash offer now",
         "meeting moved to monday", "lunch on monday?", "project report attached", "see you at the meeting"]
labels = np.array([1, 1, 1, 1, 0, 0, 0, 0])                # 1 = spam
vec = CountVectorizer().fit(texts)
Xc = vec.transform(texts)
for alpha in [1e-10, 1.0]:
    nb = MultinomialNB(alpha=alpha).fit(Xc, labels)
    p = nb.predict_proba(vec.transform(["free lunch on monday", "win a free meeting"]))[:, 1]
    print(f"alpha {alpha:g}: P(spam) for the two new messages {p.round(3)}")
