# Lesson 34: Graph Data & Network Analysis. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L34 = (34, 6, "Graph Data & Network Analysis", "Adjacency matrices, centrality and PageRank, community detection and modularity, link prediction, and graph features for ordinary models.", 50)

OBJ34 = ["Represent a network as an adjacency matrix or edge list and compute degrees",
         "Measure node importance with degree, PageRank and closeness",
         "Find communities with spectral clustering and judge them by modularity",
         "Predict links with neighbourhood scores and use graph features in a classifier"]

SRC34 = [("Page, Brin, Motwani & Winograd (1999) — The PageRank Citation Ranking", "http://ilpubs.stanford.edu:8090/422/"),
         ("Newman (2006) — Modularity and community structure in networks, PNAS", "https://www.pnas.org/doi/10.1073/pnas.0601602103"),
         ("Liben-Nowell & Kleinberg (2007) — The link-prediction problem for social networks", "https://onlinelibrary.wiley.com/doi/10.1002/asi.20591"),
         ("Blondel et al. (2008) — Fast unfolding of communities in large networks (Louvain)", "https://arxiv.org/abs/0803.0476"),
         ("Barabási — Network Science (free online book)", "http://networksciencebook.com/"),
         ("NetworkX documentation", "https://networkx.org/documentation/stable/")]

context.DEPS[34] = [3, 11, 16]
context.REFRESH[34] = "Graphs store relationships: PageRank and degree measure importance, modularity scores communities, shared neighbours predict links, and neighbour features help ordinary models."
context.FIT[34] = "Uses matrices and eigenvectors (Lesson 3), nearest-neighbour similarity (Lesson 11) and clustering (Lesson 16) on data made of connections."
context.USE[34] = (["Fraud rings and money laundering in payment networks",
                    "Friend, follower and product suggestions",
                    "Supply chains, citation networks and biological interaction networks"],
                   "Whenever relationships between entities carry information that single rows don't.",
                   "the entities really are independent: then a graph adds complexity without information.")
context.FAQ[34] = [
    ("What's the difference between PageRank and degree?",
     "Degree counts links; PageRank also weighs where they come from, so a link from an important node counts more. On directed graphs they can differ greatly."),
    ("Which community detection algorithm should I use?",
     "Louvain or Leiden for large graphs (fast modularity optimisation); spectral clustering when you know roughly how many groups there are. Check results make sense to domain experts."),
    ("When do I need graph neural networks?",
     "When node features and structure both matter and you have lots of labelled nodes. Start with graph features in an ordinary model: it's a strong baseline."),
    ("How do I store a large graph?",
     "As an edge list or a sparse matrix, never a dense adjacency matrix; graph databases help when queries follow paths."),
]
understanding.MYTHS[34] = [
    ("The most connected node is always the most important.", "Importance depends on the question: influence, reach and brokerage are measured differently."),
    ("Communities are a fixed property of the network.", "Different methods and resolutions give different, equally valid groupings."),
    ("Nodes can be split into train and test like ordinary rows.", "Connected nodes share information, so random splits can leak."),
]
extras_ex_b.MISTAKES[34] = [
    "Storing a large graph as a dense matrix.",
    "Using neighbours' labels that wouldn't be known at prediction time.",
    "Treating edges as undirected when direction matters, such as payments.",
    "Assuming preferential attachment fits every network.",
    "Reporting communities without checking modularity or whether they make sense.",
]
extras_ex_b.EX[34] = [
    ("By hand", "Edges: A–B, A–C, B–C, C–D. Give each node's degree.",
     "A 2, B 2, C 3, D 1."),
    ("By hand", "In that graph, how many common neighbours do A and D have?",
     "One: C."),
    ("By hand", "In that graph, compute the Adamic–Adar score for A and D, using the natural log.",
     "Their shared neighbour C has degree 3, so the score is 1/ln 3 ≈ 0.910."),
    ("By hand", "A graph has 20 edges, 16 of them inside communities. If random wiring would put 40% of edges inside communities, roughly what is the modularity?",
     "16/20 − 0.40 = 0.80 − 0.40 = 0.40: clear community structure."),
    ("Code", "In the community example, raise the between-community edge probability from 0.01 to 0.05. What happens to the adjusted Rand index and the modularity?",
     "Both fall, because the communities become less separated; at some point the structure is too weak for any method to recover it."),
]
checks.CHECKS[(34, 0)] = [("Degrees", [2, 2, 3, 1], "Count each node's edges (A, B, C, D).")]
checks.CHECKS[(34, 1)] = [("Common neighbours", 1, "Nodes linked to both A and D.")]
checks.CHECKS[(34, 2)] = [("Adamic–Adar", 0.910, "1 ÷ ln(degree of each shared neighbour), summed.", 0.002)]
checks.CHECKS[(34, 3)] = [("Modularity", 0.40, "Share of edges inside minus the random expectation.")]

running_code.CODE[34] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
Z = StandardScaler().fit_transform(df[["size_m2", "dist_km", "age_yrs", "price_lakh"]])
D = euclidean_distances(Z); np.fill_diagonal(D, np.inf)
A = np.zeros_like(D)
for i, row in enumerate(D):                          # link each home to its 2 most similar homes
    for j in np.argsort(row)[:2]: A[i, j] = A[j, i] = 1
same_area = (df.area.to_numpy()[:, None] == df.area.to_numpy()[None, :])
print("similarity links:", int(A.sum() // 2), " of which within the same area:", int((A * same_area).sum() // 2))
print("most connected homes (id):", df.id[np.argsort(-A.sum(axis=1))[:3]].tolist())'''
running_text.INTRO[34] = ("Turn the 12 homes into a similarity network: link each home to its 2 most similar homes on standardised size, distance, age and price. "
    "Of the 18 links, only 6 join homes in the same area: similar homes often sit in different areas, which shows that a graph built from features can reveal groupings that the area label misses. Homes 7, 2 and 4 are the most connected: typical homes that many others resemble.")

challenges.C[34] = [
    ("Degrees from an adjacency matrix", "Compute each node's degree.",
     'import numpy as np\nA = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])\n##BLANK##\nresult = deg.tolist()',
     'result', 'deg = A.sum(axis=1)', "Sum each row.",
     'deg = A.sum()  # ← sum per row, not overall'),
    ("Common neighbours", "Count the neighbours that nodes 1 and 2 share.",
     'import numpy as np\nA = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])\n##BLANK##',
     'common', 'common = int((A[1] & A[2]).sum())', "Combine the two rows with & and count.",
     'common = int(A[1].sum())  # ← count only shared neighbours'),
]

reference.GLOSSARY += [
    ("Adjacency matrix", "A matrix with a 1 where two nodes are connected and 0 otherwise.", 34, "represent"),
    ("PageRank", "A centrality score in which a node is important if important nodes link to it.", 34, "centrality"),
    ("Modularity", "How many more edges fall inside groups than random wiring with the same degrees would give.", 34, "communities"),
    ("Link prediction", "Scoring unconnected pairs of nodes by how likely they are to be connected.", 34, "links"),
    ("Homophily", "The tendency of connected nodes to be similar.", 34, "features"),
]

rai.RAI[34] = ("Guilt by association",
    "<p>Graph features judge people by their connections: friends, family, neighbours, contacts. That can be powerful for fraud detection and harmful elsewhere, penalising someone for whom they know or where they live, and it amplifies existing segregation. Be explicit about which relationships a model may use, test whether graph features act as proxies for protected attributes, and give people a way to contest decisions.</p>")
