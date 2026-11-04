# Lesson 20 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How much a single leaky feature can fake (73% accuracy on pure noise), how to process numbers, categories "
          "and text in one leak-proof pipeline, why random search usually beats grid search for the same budget, "
          "and how teams keep track of their experiments.")

QUIZ = [
    ("Target-encoding a category using averages computed on all the data, then cross-validating, gives…",
     [("a", "An honest score"), ("b", "An optimistic score, because each row's own target leaks into its feature"), ("c", "A pessimistic score")], "b",
     "On pure noise it reported 73% instead of 50%."),
    ("What does <code>ColumnTransformer</code> do?",
     [("a", "Applies different preprocessing to different columns, inside a pipeline"), ("b", "Removes columns"), ("c", "Tunes hyperparameters")], "a",
     "Numbers, categories and text each get their own steps, all fitted on training folds only."),
    ("Why does random search often beat grid search with the same number of tries?",
     [("a", "It tries many more distinct values of each setting, and usually only a few settings matter"), ("b", "It's exhaustive"), ("c", "It never overfits")], "a",
     "A grid wastes tries repeating the same few values of the important settings."),
    ("How should a learning rate between 0.001 and 1 be sampled?",
     [("a", "Uniformly"), ("b", "On a log scale"), ("c", "Only at 0.5")], "b",
     "Each order of magnitude should get similar attention; uniform sampling would mostly try values above 0.1."),
    ("Which should be logged with every training run?",
     [("a", "Only the final accuracy"), ("b", "Parameters, metrics, code and data versions, seed and library versions"), ("c", "Nothing, if the code is in git")], "b",
     "Reproducing a model needs all of them."),
]

IQ = [
    (3, "How would you build a pipeline for a table with numeric, categorical and text columns, so it can't leak?",
     "Preprocessing the whole dataframe first, then splitting.",
     "Use a <code>ColumnTransformer</code> inside a <code>Pipeline</code>: imputation and scaling for numbers, one-hot or target encoding (with cross-fitting) for categories, TF-IDF or embeddings for text, then the model. Cross-validate and tune the whole pipeline, so every statistic is learned from training folds only, and save it as one artifact so serving uses identical transformations."),
    (2, "Grid search, random search or Bayesian optimisation: which would you use?",
     "Always grid search.",
     "Grid search only for one or two settings with few values. Random search as a strong default: with the same budget it explores far more values of the settings that matter, and it parallelises trivially. Bayesian optimisation (e.g. Optuna/TPE) when each run is expensive, since it uses earlier results to pick the next settings. Add early stopping or successive halving to drop bad candidates cheaply. Report the final score with nested CV or a held-out test set."),
    (3, "Six months later, you need to reproduce the model in production exactly. What should have been recorded?",
     "\"The notebook.\"",
     "The exact code version (commit), the data snapshot or version and how it was split, every parameter and random seed, library versions (requirements or lock file), the full preprocessing pipeline, and the evaluation metrics, ideally in an experiment tracker or model registry. Without the data version and the preprocessing, the same code can produce a different model."),
]

EX = [
    ("Intermediate", "A category level appears in 4 training rows with targets $1, 1, 0, 1$. The overall average is $0.3$. Using the smoothed encoding $\\frac{n\\,\\bar{y}_{\\text{level}} + m\\,\\bar{y}}{n + m}$ with $m = 6$, what is the level's encoding?",
     "$\\bar{y}_{\\text{level}} = 0.75$. Encoding $= (4 \\times 0.75 + 6 \\times 0.3)/(4 + 6) = (3 + 1.8)/10 = 0.48$. The rare level is pulled strongly towards the overall average."),
    ("Intermediate", "A grid search over 4 learning rates, 5 depths and 3 penalties, with 5-fold CV. How many model fits is that? How many different learning rates does it try?",
     "$4 \\times 5 \\times 3 = 60$ settings $\\times\\ 5 = 300$ fits, but only 4 distinct learning rates. A random search with 60 settings would try 60."),
    ("Intermediate", "Sampling learning rates log-uniformly between 0.001 and 1, what fraction of draws fall below 0.01?",
     "The range covers 3 orders of magnitude, and 0.001 to 0.01 is one of them, so $1/3 \\approx 0.333$. (Uniform sampling would give only 0.009.)"),
]

CHECKS = {
    0: [("Smoothed encoding", 0.48, "(n·mean + m·overall) / (n + m).")],
    1: [("Model fits", 300, "settings × folds."), ("Distinct learning rates", 4, "Read it from the grid.")],
    2: [("Fraction below 0.01", 0.33333, "One of three equal-width decades on a log scale.")],
}
