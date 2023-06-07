import numpy as np
import scipy.interpolate as si

class BSplineCurve:
    
    @staticmethod
    def scipy_bspline(cv: list, n: int, degree: int) -> np.ndarray:
        """Bspline basis function using scipy

        Args:
            cv (list): list of control points.
            n (int): number of points on the curve.
            degree (int): curve degree

        Returns:
            np.ndarray: An array containing the calculated points on the curve.
        """
        
        # Prevent degree from exceeding count-1, otherwise splev will crash
        degree = np.clip(degree, 1, n - 1)

        # Create a range of u values
        c = len(cv)
        kv = np.array(
            [0] * degree + list(range(c - degree + 1)) + [c - degree] * degree,
            dtype="int",
        )
        u = np.linspace(0, c - degree, n)

        # Calculate result
        arange = np.arange(n)
        points = np.zeros((n, cv.shape[1]))
        for i in range(cv.shape[1]):
            points[arange, i] = si.splev(u, (kv, cv[:, i], degree))

        return points

    @staticmethod
    def bspline_basis(control_point_count: int, curve_point_count: int, degree: int) -> np.ndarray:
        """bspline basis function

        Args:
            c (int): number of control points.
            n (int): number of points on the curve.
            degree (int): curve degree

        Returns:
            np.ndarray: An array containing the calculated points on the curve.
        """

        # Prevent degree from exceeding count-1, otherwise splev will crash
        degree = np.clip(degree, 1, control_point_count - 1)

        # Create knot vector and a range of samples on the curve
        knot_vector = np.array(
            [0] * degree + list(range(control_point_count - degree + 1)) + [control_point_count - degree] * degree,
            dtype="int",
        )  # knot vector
        samples = np.linspace(0, control_point_count - degree, curve_point_count)  # samples range

        # Cox - DeBoor recursive function to calculate basis
        def coxDeBoor(knot_index, depth):
            if depth == 0:
                return ((samples - knot_vector[knot_index] >= 0) & (samples - knot_vector[knot_index + 1] < 0)).astype(int)

            denom1 = knot_vector[knot_index + depth] - knot_vector[knot_index]
            term1 = 0
            if denom1 > 0:
                term1 = ((samples - knot_vector[knot_index]) / denom1) * coxDeBoor(knot_index, depth - 1)

            denom2 = knot_vector[knot_index + depth + 1] - knot_vector[knot_index + 1]
            term2 = 0
            if denom2 > 0:
                term2 = (-(samples - knot_vector[knot_index + depth + 1]) / denom2) * coxDeBoor(knot_index + 1, depth - 1)

            return term1 + term2

        # Compute basis for each point
        basis_functions = np.column_stack([coxDeBoor(k, degree) for k in range(control_point_count)])
        basis_functions[-1, -1] = 1

        return basis_functions
