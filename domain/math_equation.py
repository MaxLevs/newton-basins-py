from math import prod

import numpy as np
import scipy.optimize as sopt
from sympy import symbols, diff, lambdify


class MathEquation:
    def __init__(self, roots: list[complex]):
        self.roots = roots
        """
        Roots of the polynomial equation.
        """

        self.__variable = symbols('z')
        self.__func_f = prod(map(lambda root: self.__variable - root, self.roots))
        self.__func_df = diff(self.__func_f, self.__variable)

        self.f = lambdify(self.__variable, self.__func_f, 'numpy')
        """
        A function built out of roots.
        """

        self.df_dx = lambdify(self.__variable, self.__func_df, 'numpy')
        """
        The first derivative of the function.
        """

    # noinspection PyUnresolvedReferences
    def try_find_root_from(self, z0, max_iterations: int):
        res = sopt.newton(self.f, fprime=self.df_dx, x0=z0, maxiter=max_iterations, full_output=True)
        labels = self.clusterize_approximate_roots(res.root)
        return res.root, labels

    def clusterize_approximate_roots(self, approx_roots):
        true_roots = np.array(self.roots)
        approx_errors = np.absolute(approx_roots.reshape((-1, 1)) - true_roots)
        return approx_errors.argmin(axis=1).reshape((-1, 1))

    def print_f(self):
        str(self.__func_f)

    def print_df(self):
        str(self.__func_df)
