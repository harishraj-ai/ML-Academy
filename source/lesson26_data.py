# Lesson 26: Time Series Forecasting. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L26 = (26, 5, "Time Series Forecasting", "Trend and seasonality, baselines that are hard to beat, lag features, backtesting, MASE, and forecasting several steps ahead.", 55)

OBJ26 = ["Describe a series by its trend, seasonality and noise, and compute naive, seasonal naive and moving-average baselines",
         "Turn a series into a supervised problem with past-only lag, rolling and calendar features",
         "Validate forecasts with time-ordered splits and backtesting, and report MAE and MASE",
         "Compare recursive and direct multi-step forecasting and report accuracy by horizon"]

SRC26 = [("Hyndman & Athanasopoulos — Forecasting: Principles and Practice (3rd ed.)", "https://otexts.com/fpp3/"),
         ("Hyndman & Koehler (2006) — Another look at measures of forecast accuracy", "https://www.sciencedirect.com/science/article/pii/S0169207006000239"),
         ("Makridakis, Spiliotis & Assimakopoulos (2022) — M5 accuracy competition: Results, findings, and conclusions", "https://www.sciencedirect.com/science/article/pii/S0169207021001874"),
         ("Bergmeir, Hyndman & Koo (2018) — A note on the validity of cross-validation for evaluating autoregressive time series prediction", "https://www.sciencedirect.com/science/article/pii/S0167947317302384"),
         ("scikit-learn — TimeSeriesSplit", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html"),
         ("scikit-learn — Time-related feature engineering", "https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html")]

context.DEPS[26] = [5, 6, 13]
context.REFRESH[26] = "Forecast with features built only from the past, validate by training on the past and testing on the future, and always beat a seasonal naive baseline before trusting a model."
context.FIT[26] = "Applies regression (Lesson 6) and gradient boosting (Lesson 13) to ordered data, and replaces the shuffled cross-validation of Lesson 5 with time-ordered backtesting."
context.USE[26] = (["Demand and sales forecasting for stock and staffing",
                    "Electricity load, traffic and call-centre volume planning",
                    "Budgeting, capacity planning and early warnings when a metric drifts from its forecast"],
                   "Whenever you need a number for a future date and you have a history of that number.",
                   "the future is driven by a one-off change the history never saw: then forecasts need scenarios and judgement, not just models.")
context.FAQ[26] = [
    ("How much history do I need?",
     "At least two full seasonal cycles to learn a seasonal pattern (two years for a yearly pattern), and more if you want to backtest over several periods."),
    ("Should I use ARIMA or a machine-learning model?",
     "For one series, exponential smoothing or ARIMA are strong and quick. For many related series, or when you have extra inputs such as prices and promotions, gradient boosting on lag features usually wins. Backtest both against the seasonal naive baseline."),
    ("How do I give prediction intervals?",
     "Statistical models give them directly. For ML models, train quantile models (for example <code>loss=\"quantile\"</code> in gradient boosting) or use the spread of backtest errors at each horizon."),
    ("Can I use future values of other features?",
     "Only if they'll really be known at prediction time, such as the calendar or planned promotions. A feature like \"actual temperature tomorrow\" must be replaced by the forecast you'd have had."),
]
understanding.MYTHS[26] = [
    ("A complex model will always beat a simple forecast.", "Seasonal naive and exponential smoothing often win on stable series; in this lesson, gradient boosting lost to the baseline."),
    ("Random cross-validation is fine if the model is regularised.", "Shuffling lets the model see the future; validation must respect time order."),
    ("A low MAE means a good forecast.", "MAE depends on the scale of the series; compare with a baseline using MASE."),
]
extras_ex_b.MISTAKES[26] = [
    "Shuffling rows before splitting, so the model trains on the future.",
    "Computing a rolling mean that includes the day being predicted.",
    "Not comparing with a seasonal naive baseline.",
    "Reporting one test window instead of a backtest across several.",
    "Using a tree model on a trending level without detrending or modelling changes.",
]
extras_ex_b.EX[26] = [
    ("By hand", "Daily sales for the last 8 days were 50, 52, 49, 70, 75, 51, 53, 54 (the last is yesterday). Give the naive forecast, the seasonal naive (7-day) forecast and the 3-day moving average for today.",
     "Naive: 54 (yesterday). Seasonal naive: the value 7 days before today, which is the second value, 52. Moving average: (51 + 53 + 54)/3 = 52.67."),
    ("By hand", "A model's test MAE is 18. The seasonal naive forecast's MAE on the training data is 24. Compute the MASE and say whether the model beats the baseline.",
     "MASE = 18/24 = 0.75. Below 1, so it beats the seasonal naive forecast by about 25%."),
    ("By hand", "Encode day 91 of a 365-day year as $\\sin$ and $\\cos$ of $2\\pi \\cdot 91/365$.",
     "Angle $= 2\\pi \\times 0.2493 \\approx 1.566$ radians, so $\\sin \\approx 1.000$ and $\\cos \\approx 0.004$: a quarter of the way round the circle."),
    ("By hand", "You have 730 days and use TimeSeriesSplit with 5 folds and a test size of 56 days. How many days does the first fold train on?",
     "The five test blocks cover the last 5 × 56 = 280 days, so the first fold trains on 730 − 280 = 450 days."),
    ("Code", "In the lag-feature code, drop the 7-day and 14-day lags and keep only the 1-day lag and the rolling mean. What happens to the MAE, and why?",
     "The error rises sharply, towards the naive forecast's, because the weekly pattern is carried mainly by the 7- and 14-day lags (and the weekday dummies). Which lags matter depends on the series' seasonality, so check its autocorrelation."),
]
checks.CHECKS[(26, 0)] = [("Naive", 54, "Yesterday's value."), ("Seasonal naive", 52, "The value 7 days before today."), ("3-day moving average", 52.67, "Average of the last three values.", 0.01)]
checks.CHECKS[(26, 1)] = [("MASE", 0.75, "Model MAE ÷ baseline MAE.")]
checks.CHECKS[(26, 2)] = [("sin", 1.0, "sin(2π × 91/365).", 0.005), ("cos", 0.004, "cos(2π × 91/365).", 0.005)]
checks.CHECKS[(26, 3)] = [("Training days", 450, "730 minus five test blocks of 56.")]

running_code.CODE[26] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
rng = np.random.default_rng(0)
months = pd.date_range("2023-01-01", periods=36, freq="MS")
level = df.price_lakh.mean() * (1 + 0.006 * np.arange(36)) * (1 + 0.03 * np.sin(2 * np.pi * months.month / 12))
index = pd.Series(level * rng.normal(1, 0.01, 36), index=months).round(1)   # a simulated monthly price index
test = index.index >= "2025-07-01"
naive, seasonal = index.shift(1)[test], index.shift(12)[test]
print("last 6 months:", index[test].tolist())
print("MAE, last month:", round((index[test] - naive).abs().mean(), 2), "  MAE, same month last year:", round((index[test] - seasonal).abs().mean(), 2))'''
running_text.INTRO[26] = ("The houses file has no dates, so this example simulates a monthly Chennai price index for 3 years, starting from the average price of the 12 homes, with gentle growth and a small yearly cycle. "
    "Over the last 6 months, \"same as last month\" has an MAE of 1.08 lakh, while \"same month last year\" has 4.77: here the trend dominates the weak seasonality, so the seasonal naive forecast lags a whole year of growth behind. Which baseline is best depends on the series, which is why you compute several.")

challenges.C[26] = [
    ("The seasonal naive forecast", "Forecast each of the last 7 days with the value from 7 days earlier, and compute the MAE.",
     'import numpy as np\ny = np.array([50, 52, 49, 70, 75, 51, 53, 54, 51, 50, 72, 78, 50, 55])\nactual = y[7:]\n##BLANK##\nresult = round(float(np.mean(np.abs(actual - forecast))), 2)',
     'result', 'forecast = y[:7]', "The forecast for day i is y[i - 7].",
     'forecast = actual  # ← replace with the values from 7 days earlier'),
    ("A past-only rolling mean", "Make a 3-day rolling mean that only uses days before each day (shift first).",
     'import pandas as pd\ns = pd.Series([10, 12, 14, 16, 18])\n##BLANK##\nresult = roll.tolist()[3:]',
     'result', 'roll = s.shift(1).rolling(3).mean()', "Shift by one, then roll.",
     'roll = s.rolling(3).mean()  # ← this includes the current day; fix it'),
]

reference.GLOSSARY += [
    ("Seasonality", "A pattern that repeats with a fixed period, such as day of week or month of year.", 26, "components"),
    ("Seasonal naive forecast", "A baseline forecast that repeats the value from one season earlier, such as the same day last week.", 26, "baselines"),
    ("Lag feature", "The value of a series a fixed number of steps earlier, used as a feature.", 26, "features"),
    ("Backtesting", "Evaluating forecasts by repeatedly training up to a date and forecasting the next block (rolling origin).", 26, "validation"),
    ("MASE", "Mean absolute scaled error: a forecast's MAE divided by the seasonal naive MAE on the training data; below 1 beats the baseline.", 26, "features"),
]

rai.RAI[26] = ("Forecasts become decisions",
    "<p>A demand forecast sets staffing rotas, stock in poorer neighbourhoods and hospital beds. A forecast that's systematically low for some stores or regions quietly under-serves them, and a forecast trained on a period of under-supply learns that low demand is normal. Check errors by segment, not just overall, and communicate uncertainty so planners don't treat a point forecast as a promise.</p>")
