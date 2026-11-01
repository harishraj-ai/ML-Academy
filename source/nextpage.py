# "What next: your learning plan" page.
BODY = r"""
<h2 id="learned">What you can do now</h2>
<p>If you have worked through the course, you can already do a lot:</p>
<ul>
<li><strong>Read the maths</strong> behind most ML papers' method sections: vectors, gradients, probability, loss functions (Lessons 1–4).</li>
<li><strong>Run an honest ML project</strong>: split data correctly, cross-validate, choose a metric that fits the real cost of mistakes, and avoid leakage (Lessons 5, 9, 20).</li>
<li><strong>Choose and tune a model</strong> from linear and logistic regression to trees, forests, boosting, SVMs and kNN, and explain why it works (Lessons 6–15).</li>
<li><strong>Find structure without labels</strong> with clustering and PCA (Lessons 16–17).</li>
<li><strong>Understand neural networks</strong> down to backpropagation, and how CNNs, RNNs and Transformers are built (Lessons 18–19).</li>
<li><strong>Audit a model for fairness</strong> and document it responsibly (Lesson 21).</li>
</ul>
<p>The next step is to <strong>build things on real data</strong>. Reading more is useful, but projects are where the ideas stick.</p>

<h2 id="paths">Choose a direction</h2>
<div class="table-scroll"><table class="tbl"><thead><tr><th>Direction</th><th>What the work looks like</th><th>Learn next</th></tr></thead><tbody>
<tr><td><strong>Data scientist / analyst</strong></td><td>Answer business questions with data; build and explain predictive models on tables.</td><td>SQL, pandas in depth, experiment design (A/B tests), statistics, gradient-boosting libraries (XGBoost, LightGBM), data visualisation.</td></tr>
<tr><td><strong>ML engineer</strong></td><td>Put models into production and keep them working.</td><td>Software engineering, Git, testing, APIs, Docker, cloud platforms, model monitoring and MLOps.</td></tr>
<tr><td><strong>Deep learning / AI engineer</strong></td><td>Build with neural networks and large language models.</td><td>PyTorch, computer vision and NLP, fine-tuning, retrieval-augmented generation, evaluation of LLM systems (see <a href="recent.html">Recent developments</a>).</td></tr>
<tr><td><strong>Researcher</strong></td><td>Invent and test new methods.</td><td>More linear algebra, probability and optimisation; reading and reproducing papers; a research-oriented master's or PhD.</td></tr>
<tr><td><strong>Responsible AI / policy</strong></td><td>Make sure AI systems are fair, safe, transparent and lawful.</td><td>Fairness toolkits (Fairlearn, AIF360), model documentation, AI regulation such as the EU AI Act, causal inference.</td></tr>
</tbody></table></div>

<h2 id="plan">A 12-week plan (about 6–8 hours a week)</h2>
<ol class="steps">
<li><strong>Weeks 1–2 · Consolidate.</strong> Finish the <a href="tests.html">end-of-part tests</a> and clear your <a href="review.html">review queue</a>. Redo any lesson where you scored below 80%.</li>
<li><strong>Weeks 3–4 · First real project.</strong> Pick a tabular dataset (Kaggle, the UCI repository or open government data). Do the full Lesson 20 workflow: explore, baseline, pipeline, cross-validation, test set once, short write-up.</li>
<li><strong>Weeks 5–6 · Go deeper on one family.</strong> Gradient boosting for tabular work or PyTorch for deep learning. Reproduce one tutorial exactly, then change one thing and measure the effect.</li>
<li><strong>Weeks 7–8 · Second project in a new domain.</strong> Text (classify reviews), images (a small CNN with transfer learning) or time series (forecast demand). Include a per-group evaluation and a model card.</li>
<li><strong>Weeks 9–10 · Ship it.</strong> Save the pipeline, wrap it in a small web app or API, and write down how you'd monitor it.</li>
<li><strong>Weeks 11–12 · Share and read.</strong> Publish both projects (GitHub plus a short blog post), then read one classic paper or book chapter a week from the list below.</li>
</ol>
<div class="box tip"><div class="box-title">Habits that matter more than the plan</div><ul>
<li>Always start with a simple baseline, and only keep complexity that beats it on validation data.</li>
<li>Write down what you tried and what happened — a lab notebook makes you faster and your work reproducible.</li>
<li>Explain your project to someone who isn't technical. If you can't, you don't understand it yet.</li>
</ul></div>

<h2 id="projects">Project ideas</h2>
<div class="table-scroll"><table class="tbl"><thead><tr><th>Project</th><th>Skills it practises</th><th>Course lessons</th></tr></thead><tbody>
<tr><td>Predict house or rental prices in your city</td><td>Feature engineering, regression, error analysis</td><td>6, 10, 14, 20</td></tr>
<tr><td>Customer churn or loan default with a fairness audit</td><td>Classification, threshold choice, per-group metrics, model card</td><td>8, 9, 14, 21</td></tr>
<tr><td>Spam or sentiment classifier for short texts</td><td>Text features, Naive Bayes vs logistic regression, precision–recall</td><td>8, 9, 12</td></tr>
<tr><td>Segment customers or music listening habits</td><td>Scaling, k-means, PCA visualisation, describing clusters</td><td>16, 17</td></tr>
<tr><td>Handwritten digits or clothing images with a CNN</td><td>PyTorch, convolution, overfitting control, transfer learning</td><td>18, 19</td></tr>
<tr><td>Question answering over your own notes (RAG)</td><td>Embeddings, cosine similarity, evaluating LLM answers</td><td>2, 19, Recent developments</td></tr>
</tbody></table></div>

<h2 id="resources">Free and well-regarded resources</h2>
<h3>Books</h3>
<ul>
<li><strong>An Introduction to Statistical Learning</strong> (James, Witten, Hastie, Tibshirani, Taylor) — the classic next step for classical ML; free PDF with R and Python editions.</li>
<li><strong>Mathematics for Machine Learning</strong> (Deisenroth, Faisal, Ong) — the maths of Lessons 2–4 in much more depth; free PDF.</li>
<li><strong>Dive into Deep Learning</strong> (Zhang, Lipton, Li, Smola) — an interactive deep-learning book with runnable code.</li>
<li><strong>Deep Learning</strong> (Goodfellow, Bengio, Courville) — the standard theoretical reference, free to read online.</li>
<li><strong>Fairness and Machine Learning</strong> (Barocas, Hardt, Narayanan) — the follow-on to Lesson 21; free online.</li>
<li><strong>Hands-On Machine Learning with Scikit-Learn and PyTorch</strong> (Géron) — a practical, project-driven book (paid).</li>
</ul>
<h3>Courses and practice</h3>
<ul>
<li><strong>Practical Deep Learning for Coders</strong> (fast.ai) — top-down, code-first deep learning; free.</li>
<li><strong>Neural Networks: Zero to Hero</strong> (Andrej Karpathy) — build backpropagation and a small GPT from scratch, a natural sequel to Lessons 18–19.</li>
<li><strong>Kaggle Learn</strong> — short, free hands-on courses, plus competitions and datasets for projects.</li>
<li><strong>scikit-learn user guide</strong> — clear explanations and examples for every model in this course.</li>
</ul>

<h2 id="keep">Keep the course useful</h2>
<ul>
<li>Use <a href="review.html">spaced review</a> for a few minutes a week — it keeps the core ideas from fading.</li>
<li>Keep the <a href="cheatsheet.html">cheat sheet</a> and <a href="glossary.html">glossary</a> to hand while you work on projects.</li>
<li>When you meet a new model, use <a href="guide.html">Which model?</a> and <a href="compare.html">Compare</a> to place it among the ones you know.</li>
<li>Check <a href="recent.html">Recent developments</a> for a dated overview of language models and generative AI.</li>
</ul>
"""
SOURCES = [
 ("James, Witten, Hastie, Tibshirani & Taylor — An Introduction to Statistical Learning", "https://www.statlearning.com/"),
 ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning", "https://mml-book.github.io/"),
 ("Zhang, Lipton, Li & Smola — Dive into Deep Learning", "https://d2l.ai/"),
 ("Goodfellow, Bengio & Courville — Deep Learning", "https://www.deeplearningbook.org/"),
 ("Barocas, Hardt & Narayanan — Fairness and Machine Learning", "https://fairmlbook.org/"),
 ("fast.ai — Practical Deep Learning for Coders", "https://course.fast.ai/"),
 ("Andrej Karpathy — Neural Networks: Zero to Hero", "https://karpathy.ai/zero-to-hero.html"),
 ("Kaggle Learn", "https://www.kaggle.com/learn"),
 ("Géron — Hands-On Machine Learning with Scikit-Learn and PyTorch (O'Reilly)", "https://www.oreilly.com/library/view/hands-on-machine-learning/9798341607972/"),
 ("scikit-learn — User Guide", "https://scikit-learn.org/stable/user_guide.html"),
]
