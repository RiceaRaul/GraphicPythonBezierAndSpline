import numpy as np
from bokeh.plotting import figure, show

def bspline(x, y, degree, smoothness):
    n = len(x)
    assert len(y) == n

    assert degree >= 0 and degree <= n - 1, "Invalid degree for B-spline"
    assert smoothness >= 0, "Smoothness parameter must be non-negative"

    t = np.linspace(0, 1, n + degree + 1)
    knots = np.concatenate(([0] * degree, t, [1] * degree))

    # Compute the basis functions
    def basis(i, d, t):
        if d == 0:
            return np.where(np.logical_and(t >= knots[i], t < knots[i + 1]), 1, 0)
        else:
            term1 = np.zeros_like(t)
            term2 = np.zeros_like(t)

            denominator1 = knots[i + d] - knots[i]
            nonzero_indices = denominator1 != 0
            if np.any(nonzero_indices):
                term1[nonzero_indices] = (t[nonzero_indices] - knots[i]) / denominator1[nonzero_indices] * basis(i, d - 1, t[nonzero_indices])

            denominator2 = knots[i + d + 1] - knots[i + 1]
            nonzero_indices = denominator2 != 0
            if np.any(nonzero_indices):
                term2[nonzero_indices] = (knots[i + d + 1] - t[nonzero_indices]) / denominator2[nonzero_indices] * basis(i + 1, d - 1, t[nonzero_indices])

            return term1 + term2

    # Compute the coefficients
    coeffs = []
    for i in range(n):
        b = basis(i, degree, x)
        w = np.diag(smoothness * np.ones(n))
        coeffs.append(np.linalg.lstsq(b[:, np.newaxis], y, rcond=None)[0])

    # Evaluate the spline
    xmin, xmax = x.min(), x.max()
    xx = np.linspace(xmin, xmax, 100)
    spline = np.zeros_like(xx)
    for i in range(n):
        spline += coeffs[i] * basis(i, degree, xx)

    return xx, spline

x = np.array([0., 1.2, 1.9, 3.2, 4., 6.5])
y = np.array([0., 2.3, 3., 4.3, 2.9, 3.1])
degree = 4
smoothness = 0

xx, spline = bspline(x, y, degree, smoothness)

p = figure(title='B-spline Interpolation', x_axis_label='X', y_axis_label='Y')
p.scatter(x, y, color='blue', legend_label='Original points')
p.line(xx, spline, color='red', legend_label='BSpline')

show(p)
