# Which words push towards spam? The log-ratio log P(word | spam) − log P(word | ham)
nb = MultinomialNB(alpha=1.0).fit(Xc, labels)
ratio = nb.feature_log_prob_[1] - nb.feature_log_prob_[0]
words = vec.get_feature_names_out()
order = np.argsort(ratio)
print("most spam-like:", [(str(words[i]), float(round(ratio[i], 2))) for i in order[::-1][:4]])
print("most ham-like: ", [(str(words[i]), float(round(ratio[i], 2))) for i in order[:4]])
