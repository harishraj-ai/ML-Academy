# Lesson 31: Reinforcement Learning Basics. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L31 = (31, 6, "Reinforcement Learning Basics", "Markov decision processes, the Bellman equation, value iteration, policies, Q-learning with ε-greedy exploration, and reward design.", 55)

OBJ31 = ["Describe a problem as a Markov decision process with states, actions, transitions, rewards and a discount",
         "Apply the Bellman equation and value iteration to find optimal values and a policy",
         "Implement tabular Q-learning with ε-greedy exploration",
         "Explain how reward design shapes behaviour, and when RL is the right tool"]

SRC31 = [("Sutton & Barto (2018) — Reinforcement Learning: An Introduction (2nd ed.)", "http://incompleteideas.net/book/the-book-2nd.html"),
         ("Watkins & Dayan (1992) — Q-learning, Machine Learning", "https://link.springer.com/article/10.1007/BF00992698"),
         ("Russell & Norvig — Artificial Intelligence: A Modern Approach, chapter 17", "https://aima.cs.berkeley.edu/"),
         ("Amodei et al. (2016) — Concrete Problems in AI Safety", "https://arxiv.org/abs/1606.06565"),
         ("OpenAI Spinning Up — Introduction to RL", "https://spinningup.openai.com/en/latest/spinningup/rl_intro.html"),
         ("Gymnasium — reinforcement learning environments", "https://gymnasium.farama.org/")]

context.DEPS[31] = [3, 7, 28]
context.REFRESH[31] = "RL learns from rewards by acting: the Bellman equation links each state's value to the next, value iteration solves it with a model, and Q-learning learns it from experience."
context.FIT[31] = "Extends Lesson 28's bandits to decisions that change future states, and uses the iterative update idea of gradient descent (Lesson 7)."
context.USE[31] = (["Robotics, games and simulated control",
                    "Inventory, pricing and resource allocation over time",
                    "Recommendation and ad systems that optimise long-term engagement"],
                   "Whenever decisions affect future situations and you can simulate or safely experiment.",
                   "the right answer for each case is known (supervised learning), or a single decision has no lasting effect (a bandit).")
context.FAQ[31] = [
    ("How is RL different from supervised learning?",
     "Supervised learning is told the right answer for each example. RL only gets rewards, often delayed, and its data depends on its own actions, so it must explore."),
    ("Why discount future rewards?",
     "It keeps returns finite for long tasks, reflects uncertainty about the future, and expresses a preference for sooner rewards. A $\\gamma$ near 1 means far-sighted behaviour."),
    ("What's the difference between Q-learning and SARSA?",
     "Q-learning updates towards the best next action (off-policy); SARSA updates towards the action it actually takes next (on-policy), so SARSA learns safer behaviour while exploring."),
    ("Where does deep RL fit in?",
     "When there are too many states for a table, a neural network approximates the Q function or the policy. The update rules are the same ideas as here."),
]
understanding.MYTHS[31] = [
    ("RL is the best approach for any sequential decision.", "It's data-hungry and hard to debug; simpler methods (forecast plus optimisation, bandits) are often better."),
    ("The agent will do what we mean.", "It does what maximises the reward we give, which may differ (reward hacking)."),
    ("Exploration can be switched off once training starts.", "Without exploration the agent can't discover better actions; it must keep some throughout learning."),
]
extras_ex_b.MISTAKES[31] = [
    "Designing a reward that can be maximised in an unintended way.",
    "Using no exploration, so the agent never tries better actions.",
    "Choosing a discount factor that makes the agent too short-sighted.",
    "Evaluating a policy only on the states it visited during training.",
    "Reaching for RL when a supervised model or a bandit would do.",
]
extras_ex_b.EX[31] = [
    ("By hand", "Rewards of 1, 1 and 10 arrive over three steps, with $\\gamma = 0.9$. Compute the discounted return.",
     "1 + 0.9 × 1 + 0.81 × 10 = 1 + 0.9 + 8.1 = 10.0."),
    ("By hand", "From state s, action a leads to s1 (value 5) with probability 0.8 and to s2 (value 2) with probability 0.2; every step's reward is −1; $\\gamma = 0.9$. Compute Q(s, a).",
     "0.8 × (−1 + 0.9 × 5) + 0.2 × (−1 + 0.9 × 2) = 0.8 × 3.5 + 0.2 × 0.8 = 2.8 + 0.16 = 2.96."),
    ("By hand", "Q(s, a) = 2.0. The agent gets reward 1, and the best Q in the next state is 3.0. With $\\alpha = 0.1$ and $\\gamma = 0.9$, what's the updated Q(s, a)?",
     "Target 1 + 0.9 × 3 = 3.7. Update: 2.0 + 0.1 × (3.7 − 2.0) = 2.17."),
    ("By hand", "With ε = 0.2 and 4 actions, what's the probability that an ε-greedy agent takes the action it currently thinks is best?",
     "0.8 (greedy) + 0.2 × 1/4 (chosen at random anyway) = 0.85."),
    ("Code", "In the grid world, set the slip chance to 0.3. How does the policy near the pit change?",
     "It moves further from the pit: squares next to it point away, and the long route around becomes even more attractive, because sliding into the pit is more likely."),
]
checks.CHECKS[(31, 0)] = [("Return", 10.0, "Sum of γ^t × reward.")]
checks.CHECKS[(31, 1)] = [("Q(s, a)", 2.96, "Average over outcomes of (reward + γ × next value).")]
checks.CHECKS[(31, 2)] = [("New Q", 2.17, "Q + α × (target − Q).")]
checks.CHECKS[(31, 3)] = [("Probability", 0.85, "Greedy share plus the random share that picks it.")]

running_code.CODE[31] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
# Each week a listed home sells with probability p; cutting the price 5% raises p but lowers the sale value.
p_hold = df.sold_fast.mean() / 4                     # about half the homes sell within ~4 weeks
p_cut, price, gamma, weekly_cost = min(1, 2 * p_hold), df.price_lakh.median(), 0.98, 0.5
V = {k: 0.0 for k in range(4)}                       # state: number of price cuts so far (max 3)
for _ in range(500):
    V = {k: max(p_hold * price * 0.95 ** k + (1 - p_hold) * gamma * V[k] - weekly_cost,
                p_cut * price * 0.95 ** (k + 1) + (1 - p_cut) * gamma * V[min(k + 1, 3)] - weekly_cost if k < 3 else -1e9)
         for k in V}
for k in V:
    hold = p_hold * price * 0.95 ** k + (1 - p_hold) * gamma * V[k] - weekly_cost
    print(f"after {k} cuts: value {V[k]:.1f} lakh, best action:", "hold" if abs(V[k] - hold) < 1e-9 else "cut")'''
running_text.INTRO[31] = ("Should a seller cut the price of a listed home? Treat it as a small MDP: each week the home sells with some probability (about 1 in 8, from the share of homes that sold fast), cutting the price 5% doubles that chance but lowers the sale value, and each week on the market costs 0.5 lakh. "
    "Value iteration says holding is best in every state: with these numbers, waiting a few extra weeks costs less than the 5% cut. Raise the weekly cost or the effect of a cut and the policy switches, which is exactly the kind of trade-off RL formalises.")

challenges.C[31] = [
    ("A discounted return", "Compute the discounted return of the rewards with γ = 0.5.",
     'rewards = [2, 4, 8]\ngamma = 0.5\n##BLANK##',
     'ret', 'ret = sum(r * gamma ** t for t, r in enumerate(rewards))', "Multiply each reward by γ to the power of its step.",
     'ret = sum(rewards)  # ← discount each reward'),
    ("A Q-learning update", "Apply one Q-learning update.",
     'q, r, best_next, alpha, gamma = 1.0, 0.5, 2.0, 0.5, 0.9\n##BLANK##',
     'q_new', 'q_new = q + alpha * (r + gamma * best_next - q)', "Move q towards r + γ × best_next by a fraction α.",
     'q_new = r + gamma * best_next  # ← move only a fraction alpha of the way'),
]

reference.GLOSSARY += [
    ("Markov decision process (MDP)", "A model of sequential decisions: states, actions, transition probabilities, rewards and a discount factor.", 31, "mdp"),
    ("Bellman equation", "The relation that a state's value equals the best expected reward plus discounted value of the next state.", 31, "bellman"),
    ("Value iteration", "Solving an MDP by repeatedly applying the Bellman equation to every state until values converge.", 31, "bellman"),
    ("Q-learning", "A model-free RL algorithm that learns action values from experience with temporal-difference updates.", 31, "qlearning"),
    ("Reward hacking", "An agent maximising its reward in a way its designers didn't intend.", 31, "rewards"),
]

rai.RAI[31] = ("Optimising the wrong thing at scale",
    "<p>RL systems pursue exactly the reward they're given, relentlessly. A recommender optimised for watch time can learn to promote outrage; a pricing agent can learn to exploit vulnerable customers. Choose rewards that reflect real long-term value, add constraints for things that must never happen, test policies in simulation and with small, monitored rollouts, and keep humans able to override.</p>")
