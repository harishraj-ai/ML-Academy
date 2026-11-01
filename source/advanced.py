# Advanced optional sections: ADV[lesson] = [(section_id, title, html)] — shown collapsed at the end of that section.
ADV = {
 2: [("dot-product", "Why a·b = ‖a‖‖b‖cos θ",
   "<p>Put $\\mathbf{a}$ and $\\mathbf{b}$ tail to tail; the third side of the triangle is $\\mathbf{a}-\\mathbf{b}$. Expanding with the dot product:</p>"
   "$$\\|\\mathbf{a}-\\mathbf{b}\\|^2 = (\\mathbf{a}-\\mathbf{b})\\cdot(\\mathbf{a}-\\mathbf{b}) = \\|\\mathbf{a}\\|^2 + \\|\\mathbf{b}\\|^2 - 2\\,\\mathbf{a}\\cdot\\mathbf{b}.$$"
   "<p>The law of cosines says the same side satisfies $\\|\\mathbf{a}-\\mathbf{b}\\|^2 = \\|\\mathbf{a}\\|^2 + \\|\\mathbf{b}\\|^2 - 2\\|\\mathbf{a}\\|\\|\\mathbf{b}\\|\\cos\\theta$. Comparing the two gives $\\mathbf{a}\\cdot\\mathbf{b} = \\|\\mathbf{a}\\|\\|\\mathbf{b}\\|\\cos\\theta$. Because $|\\cos\\theta|\\le 1$, it also proves the <strong>Cauchy–Schwarz inequality</strong> $|\\mathbf{a}\\cdot\\mathbf{b}| \\le \\|\\mathbf{a}\\|\\|\\mathbf{b}\\|$, which we use in Lesson 3.</p>")],
 3: [("gradient", "Why the gradient points in the direction of steepest ascent",
   "<p>The slope of $f$ in a direction given by a unit vector $\\mathbf{u}$ is the <em>directional derivative</em> $D_{\\mathbf{u}}f = \\nabla f\\cdot\\mathbf{u}$ (chain rule along the line $\\mathbf{x}+t\\mathbf{u}$). By Cauchy–Schwarz,</p>"
   "$$\\nabla f\\cdot\\mathbf{u} \\le \\|\\nabla f\\|\\,\\|\\mathbf{u}\\| = \\|\\nabla f\\|,$$"
   "<p>with equality exactly when $\\mathbf{u} = \\nabla f/\\|\\nabla f\\|$. So no direction climbs faster than the gradient, the steepest slope is $\\|\\nabla f\\|$, and $-\\nabla f$ is the steepest way down — the justification for gradient descent.</p>")],
 4: [("random-variables", "A useful identity: Var(X) = E[X²] − (E[X])²",
   "<p>Write $\\mu = E[X]$ and expand the definition, using the fact that expectation is linear:</p>"
   "$$\\operatorname{Var}(X) = E[(X-\\mu)^2] = E[X^2] - 2\\mu E[X] + \\mu^2 = E[X^2] - \\mu^2.$$"
   "<p>Check with a fair die: $E[X] = 3.5$ and $E[X^2] = (1+4+9+16+25+36)/6 = 91/6$, so $\\operatorname{Var}(X) = 91/6 - 12.25 = 35/12 \\approx 2.917$. The same identity is how libraries compute variance in one pass over the data.</p>")],
 6: [("multiple", "Deriving the normal equation, and what it means geometrically",
   "<p>With all features in a matrix $X$ (a column of 1s for the intercept) the loss is $L(\\mathbf{w}) = \\|\\mathbf{y} - X\\mathbf{w}\\|^2 = \\mathbf{y}^\\top\\mathbf{y} - 2\\mathbf{w}^\\top X^\\top\\mathbf{y} + \\mathbf{w}^\\top X^\\top X\\mathbf{w}$. Its gradient is</p>"
   "$$\\nabla L = -2X^\\top\\mathbf{y} + 2X^\\top X\\mathbf{w} = -2X^\\top(\\mathbf{y} - X\\mathbf{w}).$$"
   "<p>Setting it to zero gives the <strong>normal equation</strong> $X^\\top X\\,\\mathbf{w} = X^\\top\\mathbf{y}$, so $\\mathbf{w} = (X^\\top X)^{-1}X^\\top\\mathbf{y}$ when $X^\\top X$ is invertible (no feature is an exact combination of the others). The Hessian $2X^\\top X$ is positive semi-definite, so this is a minimum.</p>"
   "<p><strong>Geometry.</strong> $X^\\top(\\mathbf{y}-X\\mathbf{w}) = \\mathbf{0}$ says the residual vector is perpendicular to every column of $X$: the prediction $X\\mathbf{w}$ is the <em>orthogonal projection</em> of $\\mathbf{y}$ onto the space spanned by the features — the closest point to $\\mathbf{y}$ that a linear model can reach.</p>")],
 7: [("learning-rate", "When does gradient descent converge? The stability limit",
   "<p>Take the simplest bowl, $L(w) = a w^2$ with $a > 0$. Its gradient is $2aw$, so one step is</p>"
   "$$w \\leftarrow w - \\eta\\,2aw = (1 - 2\\eta a)\\,w.$$"
   "<p>After $t$ steps $w_t = (1-2\\eta a)^t w_0$, which shrinks to 0 exactly when $|1 - 2\\eta a| < 1$, i.e. $0 < \\eta < 1/a$. At $\\eta = 1/a$ it bounces forever; above, it diverges. In general the curvature is the second derivative ($2a$ here), and the rule is $\\eta < 2/\\text{curvature}$. For several weights, the curvature in the steepest direction is the largest eigenvalue $\\lambda_{\\max}$ of the Hessian, so $\\eta < 2/\\lambda_{\\max}$. For MSE linear regression the Hessian is $\\tfrac{2}{n}X^\\top X$: features on very different scales make $\\lambda_{\\max}$ huge and force a tiny learning rate — the maths behind feature scaling.</p>")],
 8: [("loss", "Where log loss comes from, and why its gradient is so simple",
   "<p>Treat each label as a coin flip with $P(y=1) = p$. The likelihood of one observation is $p^{y}(1-p)^{1-y}$, so the negative log-likelihood of the data is</p>"
   "$$-\\sum_i \\big[y_i\\ln p_i + (1-y_i)\\ln(1-p_i)\\big],$$"
   "<p>which is exactly the log loss: minimising it is <strong>maximum likelihood estimation</strong>. For the gradient, use $\\sigma'(z) = \\sigma(z)(1-\\sigma(z))$ and the chain rule on one example with $p = \\sigma(z)$, $z = \\mathbf{w}\\cdot\\mathbf{x}$:</p>"
   "$$\\frac{\\partial \\ell}{\\partial z} = -\\frac{y}{p}\\,p(1-p) + \\frac{1-y}{1-p}\\,p(1-p) = p - y, \\qquad \\frac{\\partial \\ell}{\\partial \\mathbf{w}} = (p-y)\\,\\mathbf{x}.$$"
   "<p>The Hessian is $\\sum_i p_i(1-p_i)\\,\\mathbf{x}_i\\mathbf{x}_i^\\top$, a sum of positive semi-definite matrices, so log loss is <strong>convex</strong>: gradient descent cannot get stuck in a bad local minimum.</p>")],
 9: [("roc", "Why AUC equals a ranking probability",
   "<p>Sweep the threshold from high to low. Each time it passes a positive, the ROC curve steps <em>up</em> by $1/P$; each time it passes a negative, it steps <em>right</em> by $1/N$. The area added by a negative's right-step is $\\tfrac{1}{N}\\times$(fraction of positives already passed), i.e. $\\tfrac{1}{N}\\times\\tfrac{\\#\\{\\text{positives scored above it}\\}}{P}$. Summing over all negatives:</p>"
   "$$\\text{AUC} = \\frac{1}{PN}\\sum_{\\text{neg } j}\\ \\sum_{\\text{pos } i} \\mathbb{1}[s_i > s_j] = P(\\text{random positive outscores random negative})$$"
   "<p>(ties count ½). This is the Mann–Whitney U statistic divided by $PN$ — so AUC depends only on the <em>ranking</em> of scores, not their values, which is why it ignores calibration.</p>")],
 10: [("bias-variance", "Proof of the bias–variance decomposition",
   "<p>Assume $y = f(x) + \\varepsilon$ with noise $E[\\varepsilon] = 0$, $\\operatorname{Var}(\\varepsilon) = \\sigma^2$, independent of the training set used to fit $\\hat f$. At a fixed $x$, write $\\bar f = E[\\hat f(x)]$ (averaging over training sets). Then</p>"
   "$$E\\big[(y-\\hat f)^2\\big] = E\\big[(f + \\varepsilon - \\bar f + \\bar f - \\hat f)^2\\big].$$"
   "<p>Expand the square. The cross terms vanish: $E[\\varepsilon]=0$ and $\\varepsilon$ is independent of $\\hat f$, and $E[\\bar f - \\hat f] = 0$ by definition. What remains is</p>"
   "$$E\\big[(y-\\hat f)^2\\big] = \\underbrace{\\sigma^2}_{\\text{noise}} + \\underbrace{(f-\\bar f)^2}_{\\text{bias}^2} + \\underbrace{E[(\\hat f-\\bar f)^2]}_{\\text{variance}}.$$"
   "<p>No model can remove the noise term; regularisation trades a little more bias for less variance.</p>")],
 12: [("logs", "Normalising log-scores safely: the log-sum-exp trick",
   "<p>To turn class log-scores $a_k$ into probabilities you need $P(k) = e^{a_k}/\\sum_j e^{a_j}$, but $e^{a_k}$ underflows to 0 when $a_k$ is around −800. Subtract the largest score $m = \\max_j a_j$ first:</p>"
   "$$\\log\\sum_j e^{a_j} = m + \\log\\sum_j e^{a_j - m}, \\qquad P(k) = e^{\\,a_k - m}\\Big/\\sum_j e^{a_j - m}.$$"
   "<p>Every exponent is now ≤ 0 and the largest is exactly $e^0 = 1$, so nothing overflows and the sum is at least 1. Example: scores $-1000$ and $-1001$ would both underflow, but after subtracting $m = -1000$ they become $0$ and $-1$, giving probabilities $1/(1+e^{-1}) \\approx 0.731$ and $0.269$. The same trick sits inside every softmax in Lessons 18–19.</p>")],
 13: [("split", "Why a split never increases weighted impurity",
   "<p>Gini impurity $G(\\mathbf{p}) = 1 - \\sum_k p_k^2$ and entropy $H(\\mathbf{p}) = -\\sum_k p_k\\log_2 p_k$ are <strong>concave</strong> functions of the class proportions $\\mathbf{p}$. A split sends a fraction $w_L$ of a node's examples left and $w_R = 1-w_L$ right, and the parent's proportions are the weighted average $\\mathbf{p} = w_L\\mathbf{p}_L + w_R\\mathbf{p}_R$. Concavity (Jensen's inequality) gives</p>"
   "$$G(w_L\\mathbf{p}_L + w_R\\mathbf{p}_R) \\;\\ge\\; w_L G(\\mathbf{p}_L) + w_R G(\\mathbf{p}_R),$$"
   "<p>so the information gain is always ≥ 0, and it is 0 only when both children have the same class mix as the parent. That's why a tree keeps finding \"useful\" splits all the way down to pure leaves — and why it must be stopped deliberately (Lesson 13's overfitting section).</p>")],
 14: [("gradient-boosting", "Gradient boosting is gradient descent in function space",
   "<p>Think of the predictions $F(x_1),\\dots,F(x_n)$ as the parameters. For the loss $L = \\sum_i \\tfrac12(y_i - F(x_i))^2$ the gradient with respect to each prediction is</p>"
   "$$\\frac{\\partial L}{\\partial F(x_i)} = -(y_i - F(x_i)),$$"
   "<p>so the residuals are exactly the <em>negative gradient</em>. Fitting a small tree $h$ to the residuals and updating $F \\leftarrow F + \\eta h$ is one gradient-descent step, with the tree generalising the step to new points. For any other differentiable loss, boosting fits trees to the <strong>pseudo-residuals</strong> $-\\partial L/\\partial F(x_i)$: for log loss these are $y_i - p_i$, which is how gradient-boosted classifiers work. XGBoost goes one step further and also uses the second derivatives (a Newton step).</p>")],
 15: [("kernel", "The maths behind kernels",
   "<p><strong>An explicit example.</strong> For $\\mathbf{x}, \\mathbf{z} \\in \\mathbb{R}^2$, let $\\phi(\\mathbf{x}) = (x_1^2,\\ \\sqrt2\\,x_1x_2,\\ x_2^2)$. Then</p>"
   "$$\\phi(\\mathbf{x})\\cdot\\phi(\\mathbf{z}) = x_1^2z_1^2 + 2x_1x_2z_1z_2 + x_2^2z_2^2 = (\\mathbf{x}\\cdot\\mathbf{z})^2.$$"
   "<p>So the kernel $(\\mathbf{x}\\cdot\\mathbf{z})^2$ computes a dot product in a 3-dimensional feature space without ever building $\\phi$. With $d$ features and degree $p$ the explicit space has $\\binom{d+p-1}{p}$ dimensions; the kernel still costs one dot product.</p>"
   "<p><strong>Why only dot products are needed.</strong> The SVM's optimal weights are a combination of training points, $\\mathbf{w} = \\sum_i \\alpha_i y_i \\mathbf{x}_i$ (with $\\alpha_i > 0$ only for support vectors). Substituting, the decision function becomes</p>"
   "$$f(\\mathbf{x}) = \\sum_i \\alpha_i y_i\\, K(\\mathbf{x}_i, \\mathbf{x}) + b,$$"
   "<p>and training (the <em>dual problem</em>) also uses the data only through $K(\\mathbf{x}_i,\\mathbf{x}_j)$. <strong>Mercer's condition:</strong> a function $K$ corresponds to <em>some</em> feature map exactly when every kernel matrix $[K(\\mathbf{x}_i,\\mathbf{x}_j)]$ it produces is symmetric positive semi-definite. The RBF kernel $e^{-\\gamma\\|\\mathbf{x}-\\mathbf{z}\\|^2}$ passes this test, and its feature space is infinite-dimensional.</p>")],
 16: [("kmeans", "Why k-means always stops",
   "<p>Let $J = \\sum_i \\|\\mathbf{x}_i - \\boldsymbol{\\mu}_{c(i)}\\|^2$ be the inertia for assignments $c$ and centroids $\\boldsymbol{\\mu}$.</p>"
   "<ul><li><strong>Assign step:</strong> moving each point to its nearest centroid can only lower or keep its own term, so $J$ does not increase.</li>"
   "<li><strong>Update step:</strong> for a fixed cluster, $\\sum_{i\\in C}\\|\\mathbf{x}_i - \\mathbf{m}\\|^2$ is minimised by $\\mathbf{m}$ = the mean (set its gradient $-2\\sum_{i\\in C}(\\mathbf{x}_i - \\mathbf{m})$ to zero). So $J$ does not increase.</li></ul>"
   "<p>$J$ never goes up, and there are only finitely many ways to assign $n$ points to $k$ clusters, so the algorithm cannot cycle and must stop. What's <em>not</em> guaranteed is the global minimum — finding that is NP-hard in general, which is why k-means++ starts and several restarts help.</p>")],
 17: [("algorithm", "Deriving PCA — from maximum variance and from the SVD",
   "<p><strong>Maximum variance.</strong> For centred data with covariance $C$, the variance along a unit vector $\\mathbf{u}$ is $\\mathbf{u}^\\top C\\mathbf{u}$. Maximise it subject to $\\mathbf{u}^\\top\\mathbf{u} = 1$ with a Lagrange multiplier: $\\nabla_{\\mathbf{u}}\\big[\\mathbf{u}^\\top C\\mathbf{u} - \\lambda(\\mathbf{u}^\\top\\mathbf{u}-1)\\big] = 2C\\mathbf{u} - 2\\lambda\\mathbf{u} = 0$, so $C\\mathbf{u} = \\lambda\\mathbf{u}$: $\\mathbf{u}$ must be an eigenvector, and the variance it captures is $\\mathbf{u}^\\top C\\mathbf{u} = \\lambda$. The best direction is the eigenvector with the largest eigenvalue.</p>"
   "<p><strong>Via the SVD</strong> (how libraries actually do it). Write the centred $n\\times d$ data matrix as $X = U\\Sigma V^\\top$, with $U$, $V$ orthogonal and $\\Sigma$ diagonal with singular values $s_1 \\ge s_2 \\ge \\dots$. Then</p>"
   "$$C = \\frac{X^\\top X}{n-1} = \\frac{V\\Sigma U^\\top U\\Sigma V^\\top}{n-1} = V\\,\\frac{\\Sigma^2}{n-1}\\,V^\\top.$$"
   "<p>This is an eigendecomposition of $C$: the columns of $V$ are the principal components and the eigenvalues are $\\lambda_i = s_i^2/(n-1)$. The projected data is $XV = U\\Sigma$. The SVD is preferred because it never forms $X^\\top X$, which would square the condition number and lose numerical precision.</p>")],
 18: [("backprop", "The softmax + cross-entropy gradient",
   "<p>With $K$ classes, the output layer computes $p_k = e^{z_k}/\\sum_j e^{z_j}$ and the loss for a one-hot label $\\mathbf{y}$ is $\\ell = -\\sum_k y_k\\ln p_k$. The softmax derivative is $\\partial p_k/\\partial z_j = p_k(\\mathbb{1}[k=j] - p_j)$. Therefore</p>"
   "$$\\frac{\\partial \\ell}{\\partial z_j} = -\\sum_k \\frac{y_k}{p_k}\\,p_k(\\mathbb{1}[k=j]-p_j) = -y_j + p_j\\sum_k y_k = p_j - y_j.$$"
   "<p>Exactly the same \"prediction minus target\" error signal as the sigmoid + log loss in this lesson — which is why softmax and cross-entropy are always paired, and why frameworks fuse them into one numerically stable operation.</p>")],
 19: [("transformers", "Why attention divides by √dₖ",
   "<p>Suppose the entries of a query $\\mathbf{q}$ and key $\\mathbf{k}$ are independent with mean 0 and variance 1. Then $\\mathbf{q}\\cdot\\mathbf{k} = \\sum_{i=1}^{d_k} q_ik_i$ is a sum of $d_k$ terms each with mean 0 and variance 1, so</p>"
   "$$\\operatorname{Var}(\\mathbf{q}\\cdot\\mathbf{k}) = d_k, \\qquad \\operatorname{Var}\\!\\left(\\frac{\\mathbf{q}\\cdot\\mathbf{k}}{\\sqrt{d_k}}\\right) = 1.$$"
   "<p>Without the scaling, with $d_k = 64$ the scores would have standard deviation 8; softmax of such spread-out numbers puts almost all the weight on one token, and its gradients become tiny (the softmax <em>saturates</em>). Dividing by $\\sqrt{d_k}$ keeps the scores in a range where attention can spread out and still learn — the reason given in the original Transformer paper (Vaswani et al., 2017).</p>")],
}
