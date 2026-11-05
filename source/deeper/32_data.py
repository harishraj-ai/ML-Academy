# Lesson 32 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Label spreading falls to near guessing when an irrelevant feature dominates the distances, while a supervised model with 20 labels does well; "
          "and query-by-committee, which labels the points a group of models disagrees on, only slightly beats random picks on easy data.")

QUIZ = [
    ("Why did label spreading fail on the raw features?",
     [("a", "An irrelevant, large-scale feature decided who the neighbours were"), ("b", "Too many labels"), ("c", "The classes were balanced")], "a",
     "Graph methods depend on a meaningful distance."),
    ("What fixed most of the problem?",
     [("a", "Scaling the features"), ("b", "Adding more neighbours"), ("c", "Removing labels")], "a",
     "Scaling stops one feature dominating the distances."),
    ("In query-by-committee, which points are sent for labelling?",
     [("a", "Those where the committee's models disagree most"), ("b", "Those all models agree on"), ("c", "Random points")], "a",
     "Disagreement signals uncertainty."),
    ("Why did active learning barely beat random labelling on the digits?",
     [("a", "The classes are easy and well separated, so random samples already cover them"), ("b", "The committee was too large"), ("c", "Digits can't be labelled")], "a",
     "Gains vary by problem."),
    ("Before committing a labelling budget to active learning, you should…",
     [("a", "Measure its gain over random labelling on a pilot"), ("b", "Assume it halves the cost"), ("c", "Label everything first")], "a",
     "Its benefit depends on the data."),
]

IQ = [
    (2, "When can semi-supervised learning hurt performance?",
     "\"Never; more data always helps.\"",
     "When its assumptions fail: if nearby points (under the chosen distance) don't share labels, if the classes overlap in dense regions, or if the unlabelled data comes from a different distribution than the labelled data. Bad feature scaling or irrelevant features make this common. Compare with the labelled-only baseline on a properly labelled validation set and drop the method if it doesn't help."),
]

EX = [
    ("Intermediate", "A committee of 5 models votes (3, 3, 3, 7, 7) for one digit and (1, 1, 1, 1, 1) for another. Which is more informative to label, and how many distinct votes does each have?",
     "The first, with 2 distinct votes; the second has 1, so the committee agrees."),
    ("Intermediate", "Feature 1 has standard deviation 2 and feature 2 has 100. After dividing each by its standard deviation, what is each feature's standard deviation?",
     "Both become 1, so they contribute equally to distances."),
]

CHECKS = {
    0: [("Distinct votes, first", 2, "Count the different digits voted for."), ("Distinct votes, second", 1, "All votes are the same.")],
    1: [("Feature 1", 1, "Divide by its own standard deviation."), ("Feature 2", 1, "Divide by its own standard deviation.")],
}
