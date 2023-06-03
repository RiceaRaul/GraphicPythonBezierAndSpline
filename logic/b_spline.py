import numpy as np
import scipy.interpolate as si

class BSplineCurve:
    def scipy_bspline(self, cv, n, degree):

        """ bspline basis function
            cv       = list of control points.
            n        = number of points on the curve.
            degree   = curve degree
        """
        # Prevent degree from exceeding count-1, otherwise splev will crash
        degree = np.clip(degree,1,n-1)

        # Create a range of u values
        c = len(cv)
        kv = np.array(
            [0] * degree + list(range(c - degree + 1)) + [c - degree] * degree, dtype='int')
        u = np.linspace(0, c - degree, n)

        # Calculate result
        arange = np.arange(n)
        points = np.zeros((n, cv.shape[1]))
        for i in range(cv.shape[1]):
            points[arange, i] = si.splev(u, (kv, cv[:, i], degree))

        return points

    def bspline_basis(self, c, n, degree):
        """ bspline basis function
            c        = number of control points.
            n        = number of points on the curve.
            degree   = curve degree
        """

        degree = np.clip(degree,1,c-1)
        # Create knot vector and a range of samples on the curve
        kv = np.array([0] * degree + list(range(c - degree + 1)) +
                      [c - degree] * degree, dtype='int')  # knot vector
        u = np.linspace(0, c - degree, n)  # samples range

        # Cox - DeBoor recursive function to calculate basis
        def coxDeBoor(k, d):
            # Test for end conditions
            if (d == 0):
                return ((u - kv[k] >= 0) & (u - kv[k + 1] < 0)).astype(int)

            denom1 = kv[k + d] - kv[k]
            term1 = 0
            if denom1 > 0:
                term1 = ((u - kv[k]) / denom1) * coxDeBoor(k, d - 1)

            denom2 = kv[k + d + 1] - kv[k + 1]
            term2 = 0
            if denom2 > 0:
                term2 = ((-(u - kv[k + d + 1]) / denom2) * coxDeBoor(k + 1, d - 1))

            return term1 + term2

        # Compute basis for each point
        b = np.column_stack([coxDeBoor(k, degree) for k in range(c)])
        b[-1, -1] = 1

        return b