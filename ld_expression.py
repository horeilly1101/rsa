from typing import NamedTuple


class LDSolution(NamedTuple):
    """
    This is a solution to a Linear Diophantine expression of
    the form
        ax + by,
    where x and y are integer variables.

    Note that if ax + by = g for some integer g, then there
    are infinitely many solutions x,y. You can compute any
    of the other solutions with a linear shift.
    """
    expression: "LDExpression"
    x: int
    y: int

    def shift(self, k):
        value = self.evaluate()
        return self.expression.make_solution(
            self.x + k * (self.expression.b // value),
            self.y - k * (self.expression.a // value)
        )

    def make_x_positive(self):
        if self.x > 0:
            return self

        return self.shift(1)

    def evaluate(self):
        return self.expression.evaluate(self)


class LDExpression:
    """
    Class that represents a linear diophantine expression of
    the form
        ax + by,
    where x and y are integer variables.

    LD stands for Linear Diophantine.
    """
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def __str__(self):
        return f"{self.a}x + {self.b}y"

    def __repr__(self):
        return str(self)

    def evaluate(self, solution: LDSolution):
        return self.a * solution.x + self.b * solution.y

    def make_solution(self, x, y):
        return LDSolution(self, x, y)

    def get_solution_to_gcd(self):
        """
        Compute a solution the the LDExpression that evaluates to
        the greatest common divisor of a and b. This is computed
        using Euclid's Extended Algorithm.

        e.g. find integers x,y such that
            ax + by = gcd(a, b)

        :return: LDSolution
        """
        # set initial conditions
        prev_solution = self.make_solution(1, 0)
        solution = self.make_solution(0, 1)

        while prev_solution.evaluate() % solution.evaluate():
            multiple = prev_solution.evaluate() // solution.evaluate()

            # update the stored solutions
            prev_solution, solution = (
                solution,
                self.make_solution(
                    prev_solution.x - multiple * solution.x,
                    prev_solution.y - multiple * solution.y
                )
            )

        return solution
