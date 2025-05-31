import cupy as cp
import numpy as np
import scipy.optimize as sopt

from domain.math_equation import MathEquation


# noinspection PyMethodMayBeStatic
class EquationSolver:
    def __init__(self, max_iterations : int = 100):
        self.max_iterations : int = max_iterations

    def try_find_roots(self, equation: MathEquation, z0):
        if cp.cuda.is_available():
            return self.try_find_roots_gpu(equation, z0)
        else:
            return self.try_find_roots_cpu(equation, z0)

    # noinspection PyUnresolvedReferences
    def try_find_roots_cpu(self, equation: MathEquation, z0):
        res = sopt.newton(equation.f, fprime=equation.df_dx, x0=z0, maxiter=self.max_iterations, full_output=True)
        labels = self.clusterize_approximate_roots(equation, res.root)
        return res.root, labels

    def try_find_roots_gpu(self, equation: MathEquation, z0):
        z = cp.array(z0)
        for iteration in range(self.max_iterations):
            delta = equation.f(z) / equation.df_dx(z)
            z -= delta
        labels = self.clusterize_approximate_roots(equation, z)
        return np.array(z.get()), np.array(labels.get())

    def clusterize_approximate_roots(self, equation : MathEquation, approx_roots):
        kernel = cp if cp.cuda.is_available() else np
        true_roots = kernel.array(equation.roots)
        approx_errors = kernel.absolute(approx_roots.reshape((-1, 1)) - true_roots)
        return approx_errors.argmin(axis=1).reshape((-1, 1))
