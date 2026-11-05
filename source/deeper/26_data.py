# Lesson 26 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to choose lags by looking at which past values the series correlates with (here 7, 14 and 21 days), "
          "and how to build a 90% prediction interval from held-out errors, which on a growing series actually covers only about 86%.")

QUIZ = [
    ("Why compute autocorrelation on the changes rather than the raw series?",
     [("a", "A trend makes every lag look strongly correlated"), ("b", "Changes are smaller numbers"), ("c", "It's required by pandas")], "a",
     "Removing the trend lets the seasonal peaks stand out."),
    ("The autocorrelation of daily changes peaks at 7, 14 and 21. Which lags should a model use?",
     [("a", "Lags 1 to 3"), ("b", "Multiples of 7"), ("c", "Lag 30")], "b",
     "The peaks show a weekly cycle."),
    ("A 90% interval built from held-out errors covers 86% of test values. What does that mean?",
     [("a", "The interval is too narrow for the test period"), ("b", "The model is unbiased"), ("c", "Everything is fine")], "a",
     "Coverage below the nominal level means it understates uncertainty."),
    ("Why might errors from an earlier period understate later errors?",
     [("a", "The series' level, and so its errors, is growing"), ("b", "Errors are always constant"), ("c", "Because of the random seed")], "a",
     "Relative (log) errors or recent errors fix this."),
    ("What does split conformal prediction need?",
     [("a", "A held-out calibration set of errors"), ("b", "A Bayesian prior"), ("c", "A neural network")], "a",
     "Its quantiles of errors give the interval, for any model."),
]

IQ = [
    (3, "How would you give prediction intervals for a gradient boosting forecast?",
     "\"Gradient boosting can't give intervals.\"",
     "Train quantile models (for example the 5th and 95th percentiles with a quantile loss), or use conformal prediction: compute errors on a held-out calibration period and add their quantiles to the point forecast. Either way, backtest the coverage by horizon, because errors usually grow with the horizon and with the series' level, and refresh the calibration regularly."),
]

EX = [
    ("Intermediate", "Held-out forecast errors (actual − forecast) have a 5th percentile of −12 and a 95th of 15. Tomorrow's forecast is 200. Give the 90% interval.",
     "[200 − 12, 200 + 15] = [188, 215]."),
    ("Intermediate", "A 90% interval is checked on 60 test days, and 51 of them fall inside it. What's the coverage, and is the interval too narrow or too wide?",
     "51/60 = 0.85, below 0.90, so the interval is too narrow."),
]

CHECKS = {
    0: [("Lower end", 188, "Forecast plus the 5th percentile."), ("Upper end", 215, "Forecast plus the 95th percentile.")],
    1: [("Coverage", 0.85, "Days inside ÷ days.")],
}
