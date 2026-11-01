# "Recent developments" page: large language models and generative AI. Dated; review periodically.
REVIEWED = "1 November 2026"
BODY = r"""
<div class="box warn"><div class="box-title">A dated snapshot</div><p>This field changes month by month, so this page is dated: <strong>last reviewed {REVIEWED}</strong>. The ideas (how these models are built and why they behave as they do) will last; specific products, scores and rules will not — check the linked sources for the latest. Everything here builds on <a href="lesson-19.html">Lesson 19</a>.</p></div>

<h2 id="what">What a large language model is</h2>
<p>A <strong>large language model (LLM)</strong> is a Transformer (Lesson 19) trained to do one thing: <strong>predict the next token</strong> — a word or piece of a word — given all the text before it. The loss is the cross-entropy you met in Lessons 8 and 18, minimised by gradient descent (Lesson 7) over trillions of tokens of text. Nothing more exotic is involved; the surprise is what this simple objective produces at scale.</p>
<ul>
<li><strong>Tokens and embeddings.</strong> Text is split into tokens and each token becomes a vector (Lesson 2). Attention lets every position draw on every earlier one.</li>
<li><strong>Scale.</strong> Kaplan et al. (2020) found that loss falls smoothly and predictably as parameters, data and compute grow — so-called <em>scaling laws</em>. Hoffmann et al. (2022, \"Chinchilla\") showed that many models were too big for their data, and that parameters and training tokens should grow together.</li>
<li><strong>In-context learning.</strong> GPT-3 (Brown et al., 2020) showed that a big enough model can pick up a new task from a few examples written into the prompt, with no weight updates at all.</li>
</ul>

<h2 id="assistants">From text predictor to assistant</h2>
<p>A model trained only on next-token prediction continues text; it doesn't follow instructions or decline harmful requests. Assistants are made in further stages:</p>
<ol class="steps">
<li><strong>Pre-training:</strong> next-token prediction on a huge, broad corpus — by far the most expensive stage.</li>
<li><strong>Instruction tuning:</strong> supervised fine-tuning (Lesson 19's transfer learning) on examples of requests and good responses.</li>
<li><strong>Learning from feedback:</strong> people (or other models) compare responses, and the model is trained to prefer the better ones — <em>reinforcement learning from human feedback</em> (RLHF), described for InstructGPT by Ouyang et al. (2022). ChatGPT (November 2022) brought this kind of assistant to a mass audience.</li>
</ol>

<h2 id="trends">Main trends in 2025–2026</h2>
<h3>Reasoning models and \"thinking\" at test time</h3>
<p>Instead of answering immediately, <strong>reasoning models</strong> generate a long internal chain of intermediate steps before the final answer, and are trained with reinforcement learning to make those steps lead to correct, checkable answers in maths and code. OpenAI's o1 (September 2024) popularised the approach, and DeepSeek-R1 (January 2025) published an open-weight reasoning model with a detailed report. The key idea is <strong>test-time compute</strong>: spending more computation while answering — not just while training — buys accuracy on hard problems.</p>
<h3>Agents and tool use</h3>
<p>An <strong>agent</strong> is a model that works in a loop: decide on an action, call a tool (search, run code, read a file, click in an app), look at the result, and continue until the task is done. Standard interfaces for connecting models to tools, such as the open Model Context Protocol (November 2024), spread quickly. Progress is real but uneven: Stanford's <em>AI Index 2026</em> reports that on OSWorld, a benchmark of everyday computer tasks, AI accuracy rose from about 5% in 2024 to 66.3% in 2025 — still below the 72.35% human baseline.</p>
<h3>Multimodal models</h3>
<p>Leading models now take images, audio and documents as input alongside text, and many can produce images or speech. Under the hood, images and sound are also turned into sequences of embeddings that a Transformer can attend over.</p>
<h3>Retrieval: giving models your documents</h3>
<p><strong>Retrieval-augmented generation (RAG)</strong> (Lewis et al., 2020) finds relevant passages — usually by comparing embedding vectors with cosine similarity (Lesson 2) — and puts them into the prompt, so answers can draw on current or private information and cite where they came from.</p>
<h3>Open-weight and efficient models</h3>
<p>Many capable models are released with downloadable weights, and the gap to the best closed models has narrowed; the AI Index 2026 shows the top US model ahead of the top Chinese model on the Arena leaderboard (1,503 vs 1,464) but by a small margin. Efficiency techniques let smaller models do more: <em>distillation</em> (training a small model to imitate a large one), <em>quantisation</em> (storing weights with fewer bits) and <em>mixture-of-experts</em> layers (only part of the network runs for each token).</p>

<h2 id="images">How image and video generators work</h2>
<p>Most image generators are <strong>diffusion models</strong> (Ho et al., 2020). Training takes real images, adds increasing amounts of random noise, and teaches a network to predict the noise that was added — a regression problem with an MSE loss (Lesson 6). Generation runs the process backwards: start from pure noise and repeatedly remove the predicted noise, guided by an embedding of the text prompt. Running the process in a compressed \"latent\" space (Rombach et al., 2022) made it fast enough for ordinary hardware.</p>

<h2 id="limits">Limits and risks</h2>
<ul>
<li><strong>Hallucination:</strong> fluent text is not the same as true text. Models can state false facts and invent references confidently. Check important claims against sources.</li>
<li><strong>Bias:</strong> models absorb stereotypes from their training data (see the Responsible AI notes in Lessons 5, 9 and 12).</li>
<li><strong>Security:</strong> <em>prompt injection</em> — instructions hidden in a web page or document that the model reads — can hijack an agent. Treat everything a model reads as untrusted data.</li>
<li><strong>Data and copyright:</strong> whether training on copyrighted or personal data is lawful is being decided in courts and legislatures in several countries.</li>
<li><strong>Misuse and incidents:</strong> the AI Index 2026 counts a record 362 reported AI incidents in 2025.</li>
<li><strong>Energy:</strong> training and serving large models needs large data centres; efficiency gains per query are partly offset by rapidly growing use.</li>
</ul>

<h2 id="regulation">Regulation: the EU AI Act timeline</h2>
<p>The EU AI Act is the most comprehensive AI law so far, applied in stages. According to the European Commission's official timeline (which includes the amendments of the \"Digital Omnibus on AI\"):</p>
<div class="table-scroll"><table class="tbl"><thead><tr><th>Date</th><th>What applies</th></tr></thead><tbody>
<tr><td>1 Aug 2024</td><td>The Act enters into force.</td></tr>
<tr><td>2 Feb 2025</td><td>Definitions, AI-literacy duties and prohibited practices.</td></tr>
<tr><td>2 Aug 2025</td><td>Obligations for providers of general-purpose AI models (such as LLMs).</td></tr>
<tr><td>2 Aug 2026</td><td>Enforcement begins for general-purpose AI models, prohibitions, transparency rules and AI literacy; transparency rules (Article 50) apply.</td></tr>
<tr><td>2 Dec 2026</td><td>New prohibitions on non-consensual sexual deepfakes and child sexual abuse material.</td></tr>
<tr><td>2 Dec 2027</td><td>Obligations for high-risk systems listed in Annex III (e.g. hiring, credit, education).</td></tr>
<tr><td>2 Aug 2028</td><td>Obligations for high-risk AI in regulated products (Annex I).</td></tr>
</tbody></table></div>
<p>Other countries take different approaches; the AI Index 2026 notes, for example, that public trust in government regulation of AI ranges from 91% in Singapore to 31% in the US.</p>

<h2 id="course">How this connects to the course</h2>
<div class="table-scroll"><table class="tbl"><thead><tr><th>Idea in modern AI</th><th>Where you learned the foundation</th></tr></thead><tbody>
<tr><td>Token embeddings, cosine similarity for retrieval</td><td><a href="lesson-02.html">Lesson 2: Vectors &amp; Matrices</a></td></tr>
<tr><td>Training by minimising a loss with gradients</td><td><a href="lesson-07.html">Lesson 7: Gradient Descent</a></td></tr>
<tr><td>Next-token prediction = cross-entropy over a softmax</td><td><a href="lesson-08.html">Lesson 8</a> and <a href="lesson-18.html">Lesson 18</a></td></tr>
<tr><td>Benchmarks, held-out evaluation, leakage of test data into training</td><td><a href="lesson-05.html">Lesson 5</a> and <a href="lesson-09.html">Lesson 9</a></td></tr>
<tr><td>Attention, Transformers, fine-tuning</td><td><a href="lesson-19.html">Lesson 19: Deep Learning Architectures</a></td></tr>
<tr><td>Diffusion training as noise regression</td><td><a href="lesson-06.html">Lesson 6: Linear Regression</a> (MSE)</td></tr>
</tbody></table></div>
"""
SOURCES = [
 ("Vaswani et al. (2017), Attention Is All You Need", "https://arxiv.org/abs/1706.03762"),
 ("Kaplan et al. (2020), Scaling Laws for Neural Language Models", "https://arxiv.org/abs/2001.08361"),
 ("Brown et al. (2020), Language Models are Few-Shot Learners (GPT-3)", "https://arxiv.org/abs/2005.14165"),
 ("Hoffmann et al. (2022), Training Compute-Optimal Large Language Models (Chinchilla)", "https://arxiv.org/abs/2203.15556"),
 ("Ouyang et al. (2022), Training language models to follow instructions with human feedback", "https://arxiv.org/abs/2203.02155"),
 ("OpenAI (Nov 2022), Introducing ChatGPT", "https://openai.com/index/chatgpt/"),
 ("OpenAI (Sep 2024), Learning to reason with LLMs", "https://openai.com/index/learning-to-reason-with-llms/"),
 ("DeepSeek-AI (2025), DeepSeek-R1", "https://arxiv.org/abs/2501.12948"),
 ("Anthropic (Nov 2024), Introducing the Model Context Protocol", "https://www.anthropic.com/news/model-context-protocol"),
 ("Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401"),
 ("Ho, Jain & Abbeel (2020), Denoising Diffusion Probabilistic Models", "https://arxiv.org/abs/2006.11239"),
 ("Rombach et al. (2022), High-Resolution Image Synthesis with Latent Diffusion Models", "https://arxiv.org/abs/2112.10752"),
 ("Stanford HAI (2026), The 2026 AI Index Report", "https://hai.stanford.edu/ai-index/2026-ai-index-report"),
 ("European Commission, AI Act Service Desk: implementation timeline", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act"),
]
