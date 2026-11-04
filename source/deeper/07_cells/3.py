# Gradient clipping: cap the gradient's length before stepping
def clip(g, max_norm=1.0):
    n = np.linalg.norm(g)
    return g * (max_norm / n) if n > max_norm else g

huge = np.array([300.0, -400.0])                 # an exploding gradient, length 500
print("before clipping:", huge, " length", np.linalg.norm(huge))
print("after clipping: ", clip(huge), " length", np.linalg.norm(clip(huge)))
