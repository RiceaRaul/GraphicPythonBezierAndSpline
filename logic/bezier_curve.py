import numpy as np
from scipy.special import comb
import time

class BezierCurve:

    def __init__(self, control_points):
        self.control_points = control_points

    def binomial_coefficient(self,n, k):
        coefficients = np.zeros(len(k), dtype=np.int64)
        for i, ki in enumerate(k):
            coefficients[i] = comb(n, ki, exact=True)
        return coefficients

    def calculate_curve_points(self, t):
        n = len(self.control_points) - 1

        # Calculate points on the curve
        curve_points = np.zeros((len(t), 2))
        binomial_coefficients = self.binomial_coefficient(n, np.arange(n + 1))
        for i, parameter in enumerate(t):
            bernstein_polynomials = (1 - parameter) ** (n - np.arange(n + 1)) * parameter ** np.arange(n + 1)
            curve_points[i] = np.dot(binomial_coefficients, self.control_points * bernstein_polynomials.reshape(-1, 1))

        return curve_points