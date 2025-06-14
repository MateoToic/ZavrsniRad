import numpy as np
import matplotlib.pyplot as plt

def linear_regression(X, y):
    """
    Treniraj linearnu regresiju metodom najmanjih kvadrata:
      w = (XᵀX)⁻¹ Xᵀ y
    """
    n = X.shape[0]          # uzima broj redaka od X (broj primjera)
    X_b = np.column_stack([np.ones(n), X])               # dodaj bias stupac (sve jedinice)
    w = np.linalg.pinv(X_b) @ y                 #pseudoinverz
    return X_b @ w, w