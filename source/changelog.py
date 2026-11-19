# Version history shown on changelog.html (newest first). Dates are when each release was published to the course folder.
RELEASES = [
 ("3.6", "19 November 2026", [
   "Five new animated walkthroughs: logistic regression learning its S-curve (<a href=\"lesson-08.html#boundary\">Lesson 8</a>), sweeping the threshold to trace an ROC curve (<a href=\"lesson-09.html#roc\">Lesson 9</a>), gradient boosting tree by tree (<a href=\"lesson-14.html#gradient-boosting\">Lesson 14</a>), the SVM's widest margin (<a href=\"lesson-15.html#margin\">Lesson 15</a>) and PCA's direction of most variance (<a href=\"lesson-17.html#variance-idea\">Lesson 17</a>). Ten lessons now have one.",
   "Works offline: once you have visited the published site, it keeps working without internet, and it can be installed as an app from the browser menu.",
 ]),
 ("3.5", "13 November 2026", [
   "New <a href=\"course-notes.html\">study notes</a>: notebook-style revision notes for all 36 lessons, covering every section and the Going deeper part of each lesson, explained simply with hand-drawn style sketches and worked numbers. They follow the light and dark theme.",
   "A printable PDF of the notes (<a href=\"workbook/ML-Academy-study-notes.pdf\">ML-Academy-study-notes.pdf</a>, A4, 129 pages). Your own highlights and notes stay on <a href=\"notes.html\">My notes</a>.",
   "Every Going deeper section (Lessons 2–35) is fully rewritten to be easier to follow: a question → tool table and a \"New words\" box at the start, a plain-words picture before each idea, formulas explained line by line, a \"How to read it\" note for every code output, step-by-step worked examples, and new sketches in every lesson."]),
 ("3.4", "12 November 2026", [
   "A diagram for each of Lessons 21–35, at the start of the section it explains, so every lesson from 0 to 35 now has at least one: <a href=\"lesson-21.html#sources\">where bias comes from</a>, <a href=\"lesson-22.html#joins\">joins</a>, <a href=\"lesson-23.html#random\">grid vs random search</a>, <a href=\"lesson-24.html#permutation\">permutation importance</a>, <a href=\"lesson-25.html#smote\">SMOTE</a>, <a href=\"lesson-26.html#validation\">backtesting</a>, <a href=\"lesson-27.html#mf\">matrix factorisation</a>, <a href=\"lesson-28.html#recap\">Bayes' rule</a>, <a href=\"lesson-29.html#adjust\">confounding</a>, <a href=\"lesson-30.html#lifecycle\">the model lifecycle</a>, <a href=\"lesson-31.html#mdp\">a Markov decision process</a>, <a href=\"lesson-32.html#active\">active learning</a>, <a href=\"lesson-33.html#censoring\">censoring</a>, <a href=\"lesson-34.html#represent\">graph representations</a> and <a href=\"lesson-35.html#hmm\">a hidden Markov model</a>.",
   "The diagrams work in light and dark mode and at phone width and are described for screen readers. Their captions are included in the search."]),
 ("3.3", "5 November 2026", [
   "Two new <a href=\"projects.html\">projects</a> with starter and solution notebooks: <em>Forecasting sales and catching anomalies</em> (Part 6) and <em>Did the coupon work, and who stays?</em> (Part 7), using simulated data so every answer can be checked against the truth.",
   "The <a href=\"cheatsheet.html\">formula cheat sheet</a> now covers Parts 6 and 7 (21 new formulas), <a href=\"confused.html\">commonly confused terms</a> has 16 new pairs, and the <a href=\"guide.html\">Which model?</a> guide now covers forecasting, anomalies, recommendations, survival, causal effects, sequential decisions and learning with few labels.",
   "Six new <a href=\"compare.html\">side-by-side comparisons</a> for Parts 6 and 7, five with charts computed from real models: randomised vs observational estimates, data vs concept drift, Q-learning vs SARSA, Kaplan–Meier vs ignoring censoring, semi-supervised vs active learning, and collaborative vs content-based recommendation.",
   "The review and progress pages now count all 35 lessons and 7 part tests.",
   "The home page shows the full course: 35 lessons in 7 parts, from complete beginner to advanced."]),
 ("3.2", "5 November 2026", [
   "New <strong>Part 7: Advanced topics</strong>, seven full lessons: <a href=\"lesson-29.html\">29 causal inference</a>, <a href=\"lesson-30.html\">30 MLOps: deploying &amp; monitoring models</a>, <a href=\"lesson-31.html\">31 reinforcement learning basics</a>, <a href=\"lesson-32.html\">32 semi-supervised &amp; active learning</a>, <a href=\"lesson-33.html\">33 survival analysis</a>, <a href=\"lesson-34.html\">34 graph data &amp; network analysis</a> and <a href=\"lesson-35.html\">35 graphical models &amp; hidden Markov models</a>.",
   "Each new lesson has real code and outputs, an interactive demo, worked examples, exercises with answer checking, coding challenges, a notebook, a quiz and a Going deeper section. A Part 7 test (15 questions) is on the tests page.",
   "24 new interview questions (296 in all); the complete-course route, course map, notebooks, code zip and printable workbook now cover Lessons 0–35."]),
 ("3.1", "5 November 2026", [
   "New <strong>Part 6: Intermediate topics</strong>, seven full lessons: <a href=\"lesson-22.html\">22 SQL &amp; data wrangling for ML</a>, <a href=\"lesson-23.html\">23 hyperparameter tuning</a>, <a href=\"lesson-24.html\">24 explainable AI</a>, <a href=\"lesson-25.html\">25 imbalanced data &amp; anomaly detection</a>, <a href=\"lesson-26.html\">26 time series forecasting</a>, <a href=\"lesson-27.html\">27 recommender systems</a> and <a href=\"lesson-28.html\">28 Bayesian &amp; probabilistic ML</a>.",
   "Each new lesson has real code and outputs, an interactive demo, worked examples, exercises with answer checking, a coding challenge, a notebook, a quiz and its own Going deeper section. A Part 6 test (15 questions) is on the tests page.",
   "29 new interview questions for Part 6; the complete-course route, course map, notebooks, code zip and printable workbook include Lessons 22–28."]),
 ("3.0", "4 November 2026", [
   "New <em>Going deeper</em> (intermediate) sections in 20 lessons (2–21): the linear algebra behind ML (norms, eigenvalues, SVD, condition number), calculus for optimisation (Jacobian, Hessian, convexity, Newton's method, Lagrange multipliers), statistical inference (MLE, MAP, CLT, bootstrap, A/B tests, multiple testing), trustworthy validation (nested CV, time-ordered splits, learning curves, drift), the statistics of linear regression, modern optimisers (momentum, Adam, schedules, clipping), logistic regression as a probability model (IRLS, calibration, imbalance), comparing models honestly, regularization in practice, fast neighbour search, text pipelines and generative models, tree pruning and permutation importance, tuning ensembles and XGBoost, the SVM dual and kernels, mixture models and density clustering, kernel PCA and t-SNE, making deep networks trainable, attention and residual connections from scratch, leak-proof pipelines and efficient tuning, and the fairness impossibility result measured.",
   "Each Going deeper section has real code and outputs (also in the lesson notebooks and the code zip), its own quiz, intermediate interview questions (now 232 on the interview page) and intermediate practice exercises with answer checking. In Simple reading mode it is folded behind a plain-words summary.",
   "Tables and long inline code now fit on phone screens."]),
 ("2.9", "2 November 2026", [
   "The printable workbook is regenerated: Lessons 0–21 (about 410 pages) with the <em>Make sense of it</em> boxes and the Interview corner answers, and its links now work from any copy of the course.",
   "<a href=\"downloads/ml-academy-code.zip\">All the code as a zip</a>: every lesson as a <code>.py</code> script, the coding challenges, the four projects (starter and solution), the dataset and a <code>pytest</code> suite (92 tests) that checks every script still gives the published results.",
   "Listen to this lesson: start from any section (picker, or the ▶ button next to each heading), skip a paragraph or a section back or forward (also with the [ ] { } keys), and jump anywhere with the progress bar. The controls stay at the bottom of the screen while listening.",
   "Ready for GitHub Pages: tested on a web server under a sub-folder address, with every link and file checked; README.md and requirements.txt added; the setup instructions now include pandas."]),
 ("2.8", "2 November 2026", [
   "New <strong>output checker</strong> (<code>tools/check_outputs.py</code>): re-runs every lesson and project notebook, compares each output with the published one and writes <code>tools/check_report.md</code>.",
   "New changelog and versions page (this page).",
   "Lesson 2: a code comment now shows NumPy's real output format, <code>[6 2 6]</code> (found by the new checker)."]),
 ("2.7", "2 November 2026", [
   "<a href=\"interview.html\">Hidden interview questions</a>: 158 questions with the trap and the real answer, filterable by part and level, with progress saved in your browser.",
   "<a href=\"confused.html\">Commonly confused terms</a>: 75 easily mixed-up pairs, each with the difference and a way to remember it.",
   "Every lesson has an <em>Interview corner</em> box; site search includes all questions and pairs."]),
 ("2.6", "2 November 2026", [
   "A <em>Make sense of it</em> box after all 57 worked examples: a real situation, what the result means, what-if changes (checked in Python) and why it matters in ML.",
   "22 interactive <em>What if?</em> calculators and 17 <em>Picture it</em> scenario openers across the lessons.",
   "Accessibility: maths-only table headers rewritten as text so screen readers can read them."]),
 ("2.5", "2 November 2026", [
   "New <a href=\"lesson-21.html\">Lesson 21: Ethics &amp; Fairness in Machine Learning</a>, with a two-group threshold demo, exercises, a notebook and a quiz.",
   "New <a href=\"next.html\">What next</a> page: career directions, a 12-week plan, project ideas and free resources."]),
 ("2.4", "1 November 2026", [
   "Optional advanced boxes in 16 lessons, a responsible-AI note in every lesson, and a dated <a href=\"recent.html\">Recent developments</a> page."]),
 ("2.3", "1 November 2026", [
   "Learning routes by goal, a progress dashboard, Lesson 0 (Python, NumPy and pandas refresher) and notes &amp; highlights."]),
 ("2.2", "1 November 2026", [
   "Accessibility (screen-reader descriptions, keyboard-controllable demos), reading settings, listen-to-this-lesson, the printable workbook PDF and fully offline fonts."]),
 ("2.1", "1 November 2026", [
   "Practice and feedback: exercises checked in the browser, practice problems with new numbers each time, end-of-part tests, spaced review, mini-projects and notebook coding challenges."]),
 ("2.0", "1 November 2026", [
   "The course rebuilt as a 20-lesson beginner course with explanations, maths, worked examples, interactive demos, code with real outputs, quizzes, exercises, notebooks, glossary, cheat sheet, course map and comparison pages."]),
]
NOTES = [
 "The printable workbook can't include the interactive demos and calculators; it describes each demo and points to the website.",
]
