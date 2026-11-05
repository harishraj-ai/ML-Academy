# Lesson 33 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to spot an advantage that fades over time (a hazard ratio of 0.39 early but 1.04 later), which a single Cox hazard ratio hides, "
          "and the restricted mean survival time: the average months survived within a horizon, easy to explain and assumption-free.")

QUIZ = [
    ("A group's hazard ratio is 0.4 early and 1.0 later. What's wrong with reporting one Cox hazard ratio?",
     [("a", "It averages two different effects into a number true of neither period"), ("b", "Nothing"), ("c", "Cox models can't handle groups")], "a",
     "The proportional-hazards assumption is violated."),
    ("What is the restricted mean survival time up to 12 months?",
     [("a", "The area under the survival curve from 0 to 12 months"), ("b", "The median survival"), ("c", "The hazard at 12 months")], "a",
     "It's the average time survived within the horizon."),
    ("Why is RMST useful for decision-makers?",
     [("a", "It's in time units, such as \"2 more months on average\""), ("b", "It's always larger"), ("c", "It ignores censoring")], "a",
     "It converts directly into value."),
    ("Under proportional hazards, plots of log(−log S(t)) for two groups are…",
     [("a", "Parallel"), ("b", "Crossing"), ("c", "Identical")], "a",
     "A constant hazard ratio gives a constant vertical gap."),
    ("One fix for a fading effect in a Cox model is…",
     [("a", "Separate coefficients for different time periods"), ("b", "Dropping censored data"), ("c", "Using accuracy"), ], "a",
     "Time-varying coefficients capture the change."),
]

IQ = [
    (3, "How do you check the proportional hazards assumption, and what do you do if it fails?",
     "\"It always holds for Cox models.\"",
     "Plot log(−log S(t)) by group (parallel lines under PH), test Schoenfeld residuals against time, or compare hazard ratios across time periods. If it fails: stratify by the variable, add time-varying coefficients (an interaction with time or period), or report effects that don't need the assumption, such as RMST differences or survival at fixed horizons."),
]

EX = [
    ("Intermediate", "A Kaplan–Meier curve is 1.0 from month 0 to 2, 0.8 from 2 to 5, and 0.5 from 5 to 6. Compute the restricted mean survival time up to 6 months.",
     "Area: 1.0 × 2 + 0.8 × 3 + 0.5 × 1 = 2 + 2.4 + 0.5 = 4.9 months."),
    ("Intermediate", "Group A has an RMST of 8.1 months over a year and group B 6.6. Each month a customer stays is worth 30. What's the value of the difference per customer?",
     "(8.1 − 6.6) × 30 = 1.5 × 30 = 45."),
]

CHECKS = {
    0: [("RMST", 4.9, "Sum of height × width under the curve up to 6 months.")],
    1: [("Value", 45, "Difference in months × value per month.")],
}
