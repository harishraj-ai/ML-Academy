# Lesson 35 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Forward–backward gives the probability of each hidden state on each day using the whole sequence, showing where Viterbi's single answer is uncertain, "
          "and Baum–Welch learns an HMM's probabilities from the observations alone, getting close to the true values.")

QUIZ = [
    ("What does forward–backward give that Viterbi doesn't?",
     [("a", "The probability of each state on each day, given all observations"), ("b", "The single best path"), ("c", "The transition matrix")], "a",
     "Viterbi gives one path without uncertainty."),
    ("In forward–backward, the backward pass summarises…",
     [("a", "The observations after each day"), ("b", "The observations before each day"), ("c", "Only the last day")], "a",
     "Forward covers the past; backward the future."),
    ("Baum–Welch is an example of…",
     [("a", "Expectation–maximisation"), ("b", "Gradient boosting"), ("c", "Q-learning")], "a",
     "It alternates expected counts and re-estimation."),
    ("Why scale the forward probabilities at each step?",
     [("a", "To stop them underflowing to 0 on long sequences"), ("b", "To make them sum to 2"), ("c", "To speed up Viterbi")], "a",
     "Products of many probabilities get tiny."),
    ("Why run Baum–Welch from several starting points?",
     [("a", "It can stop at a local optimum"), ("b", "It's random"), ("c", "To use more data")], "a",
     "Keep the run with the highest likelihood."),
]

IQ = [
    (3, "Explain the difference between filtering, smoothing and decoding in an HMM.",
     "Treating them as the same thing.",
     "Filtering computes P(z_t | x_1..x_t), the current state given the past only (the forward algorithm, normalised): used for real-time monitoring. Smoothing computes P(z_t | x_1..x_n), using past and future (forward–backward): more accurate, for analysis after the fact. Decoding finds the single most likely whole sequence of states (Viterbi), which can differ from picking each day's most likely state."),
]

EX = [
    ("Intermediate", "On one day, the forward value for Rainy is 0.02 and for Sunny 0.03; the backward values are 0.5 and 0.2. Compute P(rainy) that day.",
     "Products: rainy 0.02 × 0.5 = 0.010, sunny 0.03 × 0.2 = 0.006. P(rainy) = 0.010/0.016 = 0.625."),
    ("Intermediate", "Baum–Welch's expected counts give 120 sunny→sunny and 30 sunny→rainy transitions. What's the new estimate of P(rainy | sunny)?",
     "30/(120 + 30) = 0.2."),
]

CHECKS = {
    0: [("P(rainy)", 0.625, "Multiply forward and backward, then normalise.")],
    1: [("P(rainy | sunny)", 0.2, "Expected sunny→rainy ÷ all transitions from sunny.")],
}
