import numpy as np
import scipy.optimize as sopt

from domain.math_equation import MathEquation


# noinspection PyMethodMayBeStatic
class EquationSolver:
    def __init__(self, max_iterations: int):
        self.max_iterations : int = max_iterations

    # noinspection PyUnresolvedReferences
    def try_find_root_from(self, equation: MathEquation, z0):
        res = sopt.newton(equation.f, fprime=equation.df_dx, x0=z0, maxiter=self.max_iterations, full_output=True)
        labels = self.clusterize_approximate_roots(equation, res.root)
        return res.root, labels

    def clusterize_approximate_roots(self, equation : MathEquation, approx_roots):
        true_roots = np.array(equation.roots)
        approx_errors = np.absolute(approx_roots.reshape((-1, 1)) - true_roots)
        return approx_errors.argmin(axis=1).reshape((-1, 1))
