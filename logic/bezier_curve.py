import numpy as np
from scipy.special import comb

class BezierCurve:

    def __init__(self, control_points):
        self.control_points = control_points

    def binomial_coefficient(self, n: int, k: list) -> np.ndarray:
        """Calculate the binomial coefficients.

        Args:
            n (int): The total number of elements.
            k (list): The list of elements to choose from.

        Returns:
            np.ndarray: An array containing the binomial coefficients for each element in k.
        """
        coefficients = np.zeros(len(k), dtype=np.int64)
        for i, ki in enumerate(k):
            coefficients[i] = comb(n, ki, exact=True)
        return coefficients

    def calculate_curve_points(self, t: list) -> np.ndarray:
        """Calculate the points on the curve.

        Args:
            t (list): The list of parameters.

        Returns:
            np.ndarray: An array containing the calculated points on the curve.
        """
        n = len(self.control_points) - 1

        # Calculate points on the curve
        curve_points = np.zeros((len(t), 2))
        binomial_coefficients = self.binomial_coefficient(n, np.arange(n + 1))
        for i, parameter in enumerate(t):
            bernstein_polynomials = (1 - parameter) ** (n - np.arange(n + 1)) * parameter ** np.arange(n + 1)
            curve_points[i] = np.dot(binomial_coefficients, self.control_points * bernstein_polynomials.reshape(-1, 1))

        return curve_points
