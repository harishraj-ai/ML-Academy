# Lesson 29 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why adjusting for something the treatment itself causes (a mediator) can make a real effect of 12 look like 0, "
          "and how comparing people just either side of a threshold such as a credit score of 600 gives an almost experimental estimate.")

QUIZ = [
    ("A discount increases visits, and visits increase spending. What happens if you adjust for visits?",
     [("a", "You remove the part of the effect that works through visits"), ("b", "The estimate becomes more accurate"), ("c", "Nothing changes")], "a",
     "Visits are a mediator; adjusting blocks the path."),
    ("Which variable should you adjust for when estimating a treatment's effect?",
     [("a", "A collider"), ("b", "A confounder"), ("c", "A mediator")], "b",
     "Confounders cause both treatment and outcome."),
    ("Regression discontinuity compares…",
     [("a", "All treated with all untreated people"), ("b", "People just above and just below a treatment threshold"), ("c", "The same people before and after")], "b",
     "Near the threshold, the groups are nearly identical."),
    ("What would threaten a regression discontinuity design?",
     [("a", "People manipulating their score to just cross the threshold"), ("b", "A large sample"), ("c", "A linear trend in the score"), ], "a",
     "Then people just above differ systematically from those just below."),
    ("Why use only data near the threshold?",
     [("a", "Comparisons far from it mix in other differences between people"), ("b", "To save memory"), ("c", "It's required by regression")], "a",
     "There's a bias–variance trade-off in choosing the band."),
]

IQ = [
    (3, "When is adding a control variable harmful in a causal analysis?",
     "\"More controls are always better.\"",
     "When it's a mediator (caused by the treatment and affecting the outcome), adjusting removes part of the effect; when it's a collider (caused by both treatment and outcome, or their causes), adjusting creates a spurious association. Adjust for pre-treatment confounders. A causal diagram, drawn from domain knowledge before looking at the results, decides which is which."),
]

EX = [
    ("Intermediate", "Customers with a score of 600 or more get an offer. Just below 600, average spend is 80; just above, 92, and the trend in spend is flat near the threshold. Estimate the effect.",
     "About 92 − 80 = 12, the jump at the threshold."),
    ("Intermediate", "A treatment's total effect is 10, and 6 of it works through a mediator. What does a regression that adjusts for the mediator estimate?",
     "The direct effect, 10 − 6 = 4."),
]

CHECKS = {
    0: [("Effect", 12, "The jump at the cut-off.")],
    1: [("Direct effect", 4, "Total minus the part through the mediator.")],
}
