import numpy as np

def f(v):                                  # a function from 2 numbers to 2 numbers
    x, y = v
    return np.array([x**2 * y, 5 * x + np.sin(y)])

def jacobian_formula(v):
    x, y = v
    return np.array([[2 * x * y, x**2],    # row 1: ∂f1/∂x, ∂f1/∂y
                     [5.0, np.cos(y)]])    # row 2: ∂f2/∂x, ∂f2/∂y

def jacobian_numeric(f, v, h=1e-6):
    cols = [(f(v + h * e) - f(v - h * e)) / (2 * h) for e in np.eye(len(v))]
    return np.column_stack(cols)

v = np.array([1.0, 2.0])
print(jacobian_formula(v).round(4))
print(jacobian_numeric(f, v).round(4))
