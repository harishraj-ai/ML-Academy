import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import TargetEncoder

# A category with 2,000 levels (like a postcode) that has NO real link to the target
rng = np.random.default_rng(0)
n = 5000
code = rng.integers(0, 2000, n)
y = rng.integers(0, 2, n)
cv = KFold(5, shuffle=True, random_state=0)

# Wrong: encode with each level's average target computed on ALL the data, then cross-validate
means = pd.Series(y).groupby(code).mean()
leaky = means[code].to_numpy()[:, None]
print("naive target encoding, CV accuracy:", round(cross_val_score(LogisticRegression(), leaky, y, cv=cv).mean(), 3))

# Right: TargetEncoder inside the pipeline (it also uses internal cross-fitting when training)
pipe = make_pipeline(TargetEncoder(cv=KFold(5, shuffle=True, random_state=0)), LogisticRegression())
print("target encoding inside the pipeline, CV accuracy:", round(cross_val_score(pipe, code[:, None], y, cv=cv).mean(), 3))
