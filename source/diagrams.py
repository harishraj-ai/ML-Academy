# One explanatory SVG diagram per lesson: (section id to place it in, svg, caption).
# Colours come from CSS classes so the figures follow light/dark theme.
D = {}

def box(x, y, w, h, text, cls="b", sub=None):
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cls}"/>'
    if sub:
        t += f'<text x="{x+w/2}" y="{y+h/2-4}" class="t c">{text}</text><text x="{x+w/2}" y="{y+h/2+14}" class="t c s">{sub}</text>'
    else:
        t += f'<text x="{x+w/2}" y="{y+h/2+5}" class="t c">{text}</text>'
    return t

def arr(x1, y1, x2, y2, cls="ln"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#ah)"/>'

DEFS = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fa"/></marker></defs>'

def svg(w, h, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'

# 1 — rules vs learning
D[1] = ("rules-vs-learning", svg(640, 260,
    '<text x="20" y="24" class="t h">Traditional programming</text>' +
    box(20, 38, 110, 38, "Rules") + box(20, 86, 110, 38, "Data") + arr(130, 57, 215, 75) + arr(130, 105, 215, 87) +
    box(220, 58, 150, 44, "Program", "b") + arr(370, 80, 440, 80) + box(445, 58, 150, 44, "Answers", "b3") +
    '<line x1="20" y1="142" x2="620" y2="142" class="dash"/>' +
    '<text x="20" y="168" class="t h">Machine learning</text>' +
    box(20, 180, 110, 34, "Data") + box(20, 220, 110, 34, "Answers", "b3") + arr(130, 197, 215, 212) + arr(130, 237, 215, 222) +
    box(220, 195, 150, 44, "Learning algorithm", "b") + arr(370, 217, 440, 217) + box(445, 195, 150, 44, "Model (the rules)", "b2")),
    "Traditional programming turns hand-written rules into answers. Machine learning turns examples (data plus answers) into the rules — a trained model that can then answer new cases.")

# 2 — vector addition
D[2] = ("vector-ops", svg(420, 260,
    '<line x1="40" y1="220" x2="400" y2="220" class="ax"/><line x1="40" y1="220" x2="40" y2="20" class="ax"/>' +
    '<line x1="40" y1="220" x2="80" y2="140" class="la" marker-end="url(#ah)"/><text x="12" y="170" class="t a">a = (1, 2)</text>' +
    '<line x1="80" y1="140" x2="200" y2="180" class="lv" marker-end="url(#ah)"/><text x="130" y="145" class="t v">b = (3, −1)</text>' +
    '<line x1="40" y1="220" x2="200" y2="180" class="lw" marker-end="url(#ah)"/><text x="120" y="214" class="t w">a + b = (4, 1)</text>' +
    ''.join(f'<text x="{40+i*40-3}" y="238" class="t s">{i}</text>' for i in range(0, 9, 2))),
    "Adding vectors: walk along a, then along b; the sum goes straight from start to finish (axis ticks every 2 units, drawn at 40 px per unit).")

# 3 — tangent and gradient direction
D[3] = ("derivative", svg(440, 260,
    '<line x1="30" y1="225" x2="420" y2="225" class="ax"/>' +
    '<path d="M40,30 Q230,400 420,30" class="lv2" fill="none"/>' +
    '<line x1="60" y1="85" x2="182" y2="222" class="lw"/>' +
    '<circle cx="120" cy="153" r="6" class="fa2"/>' +
    '<text x="132" y="140" class="t">tangent: slope f′(x) &lt; 0 here</text>' +
    '<line x1="120" y1="246" x2="190" y2="246" class="la" marker-end="url(#ah)"/><text x="196" y="250" class="t a">step: x ← x − η f′(x)</text>' +
    '<circle cx="230" cy="215" r="5" class="fa"/><text x="290" y="218" class="t s">minimum: f′(x) = 0</text>'),
    "The derivative is the slope of the tangent line. Where the slope is negative, gradient descent moves right — downhill — until the slope is zero at the minimum.")

# 4 — Bayes tree
D[4] = ("bayes", svg(640, 250,
    box(250, 10, 140, 44, "1,000 people") +
    arr(290, 54, 150, 98) + arr(350, 54, 490, 98) +
    box(70, 100, 160, 44, "10 sick", "b3", "1% prior") + box(410, 100, 160, 44, "990 healthy", "b") +
    arr(120, 144, 70, 188) + arr(180, 144, 230, 188) + arr(460, 144, 410, 188) + arr(520, 144, 570, 188) +
    box(10, 190, 120, 50, "9 test +", "b2", "90% sensitivity") + box(170, 190, 110, 50, "1 test −", "b") +
    box(350, 190, 120, 50, "49.5 test +", "b4", "5% false +") + box(500, 190, 130, 50, "940.5 test −", "b")),
    "Of about 58.5 positive tests, only 9 come from sick people: P(sick | positive) ≈ 9 / 58.5 ≈ 15%.")

# 5 — splits and k-fold
D[5] = ("cross-validation", svg(640, 220,
    '<text x="10" y="22" class="t h">Hold-out split</text>' +
    '<rect x="10" y="32" width="420" height="30" class="b2"/><text x="220" y="52" class="t c">training 70%</text>' +
    '<rect x="430" y="32" width="90" height="30" class="b3"/><text x="475" y="52" class="t c">val 15%</text>' +
    '<rect x="520" y="32" width="90" height="30" class="b4"/><text x="565" y="52" class="t c">test 15%</text>' +
    '<text x="10" y="96" class="t h">5-fold cross-validation (on the training part)</text>' +
    ''.join(f'<text x="10" y="{124+i*20}" class="t s">run {i+1}</text>' + ''.join(f'<rect x="{70+j*108}" y="{110+i*20}" width="104" height="16" class="{"b3" if i==j else "b2"}"/>' for j in range(5)) for i in range(5))),
    "Top: the three-way split. Bottom: in k-fold cross-validation, each fold (orange) takes one turn as the validation set while the other folds train the model.")

# 6 — residuals
D[6] = ("loss", svg(440, 250,
    '<line x1="30" y1="220" x2="420" y2="220" class="ax"/><line x1="30" y1="220" x2="30" y2="20" class="ax"/>' +
    '<line x1="30" y1="160" x2="420" y2="40" class="la"/>' +
    ''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{160-(x-30)*120/390}" class="lr"/><circle cx="{x}" cy="{y}" r="6" class="fv"/>' for x, y in [(80, 120), (150, 150), (220, 80), (290, 110), (360, 50)]) +
    '<text x="300" y="185" class="t r">residual = y − ŷ</text><text x="320" y="38" class="t a">ŷ = wx + b</text>'),
    "Each red segment is a residual — the gap between a data point and the line. Least squares minimises the sum of their squares.")

# 7 — learning rates
def bowl(ox, title, pts):
    path = f'<path d="M{ox+10},30 Q{ox+100},250 {ox+190},30" class="lv2" fill="none"/>'
    p = ''.join(f'<circle cx="{ox+x}" cy="{y}" r="4" class="fa"/>' for x, y in pts)
    l = ''.join(f'<line x1="{ox+pts[i][0]}" y1="{pts[i][1]}" x2="{ox+pts[i+1][0]}" y2="{pts[i+1][1]}" class="lw2"/>' for i in range(len(pts)-1))
    return path + l + p + f'<text x="{ox+100}" y="200" class="t c">{title}</text>'
D[7] = ("learning-rate", svg(640, 215,
    bowl(0, "too small: slow", [(25, 64), (34, 81), (42, 94), (49, 105), (55, 112)]) +
    bowl(215, "just right", [(25, 64), (70, 128), (95, 139.7), (100, 140)]) +
    bowl(430, "too large: diverges", [(85, 137), (125, 131.5), (60, 118), (160, 91), (20, 53)])),
    "The same loss bowl with three learning rates: tiny steps crawl, good steps converge, and steps that are too big overshoot further each time.")

# 8 — sigmoid
D[8] = ("sigmoid", svg(440, 230,
    '<line x1="30" y1="200" x2="420" y2="200" class="ax"/><line x1="225" y1="200" x2="225" y2="20" class="ax"/>' +
    '<line x1="30" y1="30" x2="420" y2="30" class="dash"/><line x1="30" y1="115" x2="420" y2="115" class="dash"/>' +
    '<path d="' + 'M' + ' L'.join(f'{30+i*3.9:.1f},{200-170/(1+2.718**(-(i-50)/8)):.1f}' for i in range(101)) + '" class="la" fill="none"/>' +
    '<text x="34" y="26" class="t s">p = 1</text><text x="34" y="111" class="t s">p = 0.5 (threshold)</text><text x="34" y="196" class="t s">p = 0</text>' +
    '<text x="232" y="215" class="t s">z = 0</text><text x="300" y="80" class="t a">predict 1</text><text x="80" y="160" class="t v">predict 0</text>'),
    "The sigmoid turns any score z into a probability. With threshold 0.5, the decision boundary is exactly where z = 0.")

# 9 — confusion matrix
D[9] = ("confusion", svg(420, 250,
    '<text x="250" y="22" class="t c h">predicted</text><text x="185" y="48" class="t c">positive</text><text x="315" y="48" class="t c">negative</text>' +
    '<text x="40" y="150" class="t c h" transform="rotate(-90 40 150)">actual</text>' +
    '<text x="95" y="108" class="t c">positive</text><text x="95" y="198" class="t c">negative</text>' +
    box(120, 60, 130, 85, "TP = 8", "b2", "caught") + box(250, 60, 130, 85, "FN = 2", "b4", "missed") +
    box(120, 150, 130, 85, "FP = 10", "b4", "false alarm") + box(250, 150, 130, 85, "TN = 80", "b2", "correctly ignored")),
    "The screening-test example from this lesson. Green cells are correct; red cells are the two kinds of mistakes.")

# 10 — dartboards
def board(cx, label, pts):
    rings = ''.join(f'<circle cx="{cx}" cy="95" r="{r}" class="ring"/>' for r in (60, 40, 20))
    return rings + f'<circle cx="{cx}" cy="95" r="5" class="fa"/>' + ''.join(f'<circle cx="{cx+x}" cy="{95+y}" r="4" class="fv"/>' for x, y in pts) + f'<text x="{cx}" y="182" class="t c">{label}</text>'
D[10] = ("bias-variance", svg(640, 195,
    board(80, "low bias, low var.", [(-5, 3), (4, -4), (2, 6), (-3, -5), (6, 1)]) +
    board(240, "high bias, low var.", [(30, -25), (36, -20), (28, -30), (34, -32), (39, -26)]) +
    board(400, "low bias, high var.", [(-40, 10), (35, -30), (10, 42), (-25, -38), (40, 25)]) +
    board(560, "high bias, high var.", [(20, -45), (48, -5), (30, -30), (55, -35), (10, -20)])),
    "Each dot is a model trained on a different training set; the centre is the truth. Bias is being off-centre on average; variance is the scatter.")

# 11 — kNN
D[11] = ("algorithm", svg(420, 240,
    '<circle cx="210" cy="120" r="72" class="dash2"/>' +
    ''.join(f'<line x1="210" y1="120" x2="{x}" y2="{y}" class="ln2"/>' for x, y in [(170, 90), (250, 150), (240, 70)]) +
    ''.join(f'<circle cx="{x}" cy="{y}" r="7" class="fa"/>' for x, y in [(170, 90), (240, 70), (90, 60), (60, 140), (110, 200)]) +
    ''.join(f'<circle cx="{x}" cy="{y}" r="7" class="fv"/>' for x, y in [(250, 150), (330, 170), (350, 90), (300, 210)]) +
    '<text x="203" y="127" class="t h">✚</text><text x="12" y="22" class="t s">k = 3 neighbours: 2 green, 1 purple → predict green</text>'),
    "kNN with k = 3: the query (✚) takes a vote of its three nearest training points; the dashed circle reaches the third neighbour.")

# 12 — naive bayes flow
D[12] = ("spam-example", svg(640, 150,
    box(10, 50, 130, 50, "\"free money now\"") + arr(140, 75, 175, 75) +
    box(180, 10, 150, 40, "P(free | spam)", "b2") + box(180, 55, 150, 40, "P(money | spam)", "b2") + box(180, 100, 150, 40, "P(now | spam)", "b2") +
    arr(330, 75, 365, 75) + box(370, 50, 120, 50, "× P(spam)", "b3", "multiply") + arr(490, 75, 520, 75) + box(525, 50, 105, 50, "compare", "b", "spam vs ham")),
    "Naive Bayes multiplies the prior with one probability per word for each class (shown for spam; ham is computed the same way), then picks the larger.")

# 13 — tree diagram
D[13] = ("structure", svg(560, 220,
    box(190, 10, 180, 46, "petal width ≤ 0.8?") +
    arr(240, 56, 130, 100) + arr(320, 56, 420, 100) + '<text x="165" y="80" class="t s">yes</text><text x="385" y="80" class="t s">no</text>' +
    box(60, 102, 140, 46, "setosa", "b2") + box(340, 102, 180, 46, "petal width ≤ 1.75?") +
    arr(390, 148, 330, 170) + arr(470, 148, 510, 170) +
    box(240, 172, 150, 44, "versicolor", "b2") + box(410, 172, 140, 44, "virginica", "b2")),
    "The depth-2 iris tree from this lesson. Internal nodes ask questions; leaves (green) give the prediction.")

# 14 — bagging vs boosting
D[14] = ("compare", svg(640, 250,
    '<text x="10" y="22" class="t h">Bagging / random forest — parallel</text>' +
    ''.join(box(10+i*105, 35, 95, 38, f"tree {i+1}", "b2") + arr(57+i*105, 73, 270, 110) for i in range(3)) +
    '<text x="330" y="58" class="t s">each on its own bootstrap sample</text>' + box(220, 112, 110, 34, "vote / average", "b3") +
    '<text x="10" y="178" class="t h">Boosting — sequential</text>' +
    box(10, 192, 100, 40, "tree 1", "b2") + arr(110, 212, 140, 212) + box(145, 192, 140, 40, "tree 2", "b2", "fits tree 1's errors") + arr(285, 212, 315, 212) +
    box(320, 192, 140, 40, "tree 3", "b2", "fits remaining errors") + arr(460, 212, 490, 212) + box(495, 192, 130, 40, "weighted sum", "b3")),
    "Bagging trains trees independently and averages them (cuts variance). Boosting trains each tree to fix what the previous ones got wrong (cuts bias).")

# 15 — SVM margin
D[15] = ("margin", svg(440, 260,
    '<polygon points="60,250 170,10 270,10 160,250" class="road"/>' +
    '<line x1="110" y1="250" x2="220" y2="10" class="lw"/>' +
    '<line x1="60" y1="250" x2="170" y2="10" class="dash"/><line x1="160" y1="250" x2="270" y2="10" class="dash"/>' +
    ''.join(f'<circle cx="{x}" cy="{y}" r="7" class="fv"/>' for x, y in [(60, 80), (40, 160), (100, 40), (88, 190)]) +
    ''.join(f'<circle cx="{x}" cy="{y}" r="7" class="fa"/>' for x, y in [(330, 120), (300, 200), (380, 60), (360, 180)]) +
    '<circle cx="124" cy="110" r="7" class="fv"/><circle cx="124" cy="110" r="12" class="ring2"/>' +
    '<circle cx="233" cy="110" r="7" class="fa"/><circle cx="233" cy="110" r="12" class="ring2"/>' +
    '<text x="300" y="30" class="t s">margin = 2 / ‖w‖</text><text x="245" y="138" class="t s">support vectors (ringed)</text>'),
    "The SVM boundary (solid) runs down the middle of the widest possible road. Only the points on the road's edges — the support vectors — fix its position.")

# 16 — dendrogram
D[16] = ("hierarchical", svg(460, 220,
    ''.join(f'<text x="{40+i*70}" y="210" class="t c">{c}</text>' for i, c in enumerate("ABCDEF")) +
    '<path d="M40,190 V160 H110 V190" class="ln3"/><path d="M180,190 V150 H250 V190" class="ln3"/>' +
    '<path d="M75,160 V110 H215 V150" class="ln3"/><path d="M320,190 V140 H390 V190" class="ln3"/>' +
    '<path d="M145,110 V50 H355 V140" class="ln3"/>' +
    '<line x1="20" y1="80" x2="440" y2="80" class="dash"/><text x="362" y="74" class="t s">cut → 2 clusters</text>'),
    "A dendrogram records every merge (lower = merged earlier, more similar). Cutting at the dashed line gives 2 clusters: {A, B, C, D} and {E, F}.")

# 17 — PCA axes
D[17] = ("variance-idea", svg(440, 250,
    '<ellipse cx="220" cy="125" rx="170" ry="45" transform="rotate(-25 220 125)" class="ell"/>' +
    ''.join(f'<circle cx="{220+x}" cy="{125+y}" r="4" class="fv"/>' for x, y in [(-140, 60), (-100, 30), (-60, 40), (-30, 0), (0, 10), (30, -20), (70, -20), (100, -50), (140, -60), (-80, 55), (50, 5), (-20, 25), (110, -30)]) +
    '<line x1="220" y1="125" x2="380" y2="50" class="la" marker-end="url(#ah)"/><text x="350" y="40" class="t a">PC1 (most variance)</text>' +
    '<line x1="220" y1="125" x2="250" y2="190" class="lv" marker-end="url(#ah)"/><text x="255" y="205" class="t v">PC2</text>'),
    "PCA rotates the axes: PC1 points along the data's longest spread; PC2 is perpendicular and captures what's left.")

# 18 — network diagram
def node(x, y, label, cls="b"):
    return f'<circle cx="{x}" cy="{y}" r="24" class="{cls}"/><text x="{x}" y="{y+5}" class="t c">{label}</text>'
D[18] = ("forward", svg(560, 250,
    ''.join(f'<line x1="{100}" y1="{yi}" x2="{280}" y2="{yh}" class="ln2"/>' for yi in (70, 180) for yh in (70, 180)) +
    '<line x1="280" y1="70" x2="460" y2="125" class="ln2"/><line x1="280" y1="180" x2="460" y2="125" class="ln2"/>' +
    '<text x="180" y="62" class="t s">0.5</text><text x="128" y="104" class="t s">−0.5</text><text x="128" y="160" class="t s">0.3</text><text x="180" y="198" class="t s">0.8</text>' +
    '<text x="370" y="88" class="t s">v₁ = 1</text><text x="370" y="170" class="t s">v₂ = −1</text>' +
    node(100, 70, "x₁=1") + node(100, 180, "x₂=0") + node(280, 70, "0.62", "b2") + node(280, 180, "0.38", "b2") + node(460, 125, "0.56", "b3") +
    '<text x="100" y="230" class="t c s">inputs</text><text x="280" y="230" class="t c s">hidden (sigmoid)</text><text x="460" y="230" class="t c s">output p</text>'),
    "The 2-2-1 network from the worked example, with its weights and the values from the forward pass.")

# 19 — CNN pipeline
D[19] = ("cnn", svg(640, 170,
    '<rect x="10" y="40" width="80" height="80" class="b"/><text x="50" y="140" class="t c s">image 28×28</text>' +
    arr(92, 80, 118, 80) + ''.join(f'<rect x="{122+i*6}" y="{40+i*4}" width="70" height="70" class="b2"/>' for i in range(4)) + '<text x="175" y="140" class="t c s">conv: 16 maps</text>' +
    arr(220, 80, 246, 80) + ''.join(f'<rect x="{250+i*5}" y="{55+i*3}" width="40" height="40" class="b2"/>' for i in range(4)) + '<text x="280" y="140" class="t c s">pool 14×14</text>' +
    arr(312, 80, 338, 80) + ''.join(f'<rect x="{342+i*4}" y="{60+i*2}" width="30" height="30" class="b3"/>' for i in range(6)) + '<text x="375" y="140" class="t c s">conv + pool 7×7</text>' +
    arr(400, 80, 426, 80) + '<rect x="430" y="20" width="18" height="120" class="b"/><text x="439" y="160" class="t c s">flatten</text>' +
    arr(450, 80, 486, 80) + ''.join(f'<circle cx="510" cy="{30+i*14}" r="5" class="fa"/>' for i in range(8)) + '<text x="560" y="84" class="t s">10 class</text><text x="560" y="100" class="t s">scores</text>'),
    "A typical small CNN: convolution and pooling layers shrink the image while increasing the number of feature maps, then a dense layer scores each class.")

# 20 — pipeline
D[20] = ("pipelines", svg(640, 230,
    box(10, 90, 100, 50, "raw data") + arr(110, 115, 140, 115) +
    box(145, 85, 110, 60, "add_features", "b", "ratios, logs") + arr(255, 115, 285, 115) +
    '<rect x="290" y="10" width="220" height="210" rx="12" class="dash2"/><text x="400" y="30" class="t c s">ColumnTransformer</text>' +
    box(305, 45, 90, 40, "impute", "b2") + box(405, 45, 90, 40, "scale", "b2") + '<text x="400" y="100" class="t c s">numeric columns</text>' +
    box(305, 130, 90, 40, "impute", "b3") + box(405, 130, 90, 40, "one-hot", "b3") + '<text x="400" y="190" class="t c s">categorical columns</text>' +
    arr(510, 115, 540, 115) + box(545, 90, 85, 50, "model", "b4")),
    "The final project's pipeline. Fitting it learns every step from the training data only; the same object then turns raw rows into predictions.")
