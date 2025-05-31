from math import prod

import sympy as sp


class MathEquation:
    """
    Basic representation of Math equation.
    """

    def __init__(self, roots: list[complex], f, df_dx):
        self.roots = roots
        """
        Roots of the polynomial equation.
        """
        self.f = f
        """
        A function built out of roots.
        """
        self.df_dx = df_dx
        """
        The first derivative of the function.
        """


class PolynomialMathEquation(MathEquation):
    """
    Representation of polynomial Math equation.
    """

    def __init__(self, roots: list[complex]):
        self.__variable = sp.symbols('z')
        self.__func_f = prod(map(lambda root: self.__variable - root, roots))
        self.__func_df = sp.diff(self.__func_f, self.__variable)

        f = sp.lambdify(self.__variable, self.__func_f, 'numpy')
        df_dx = sp.lambdify(self.__variable, self.__func_df, 'numpy')
        super().__init__(roots, f, df_dx)

    def print_f(self):
        str(self.__func_f)

    def print_df(self):
        str(self.__func_df)
