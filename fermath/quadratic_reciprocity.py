from fermath.factorizations.prime_factorization import PrimeFactorization
from fermath.factorizations.even_factorization import EvenFactorization
from fermath.primality_testing import is_prime


def get_quadratic_non_residue(number: int) -> int:
    """
    :param number: positive integer greater than 2
    :return: a quadratic non residue mod number
    """
    for i in range(2, number):
        if compute_jacobi_symbol(i, number) == -1:
            return i

    raise ValueError(f"No quadratic non residues of {number} found!")


def is_quadratic_residue(x, modulus) -> bool:
    if is_prime(modulus):
        return compute_jacobi_symbol(x, modulus)

    raise ValueError()


def compute_jacobi_symbol(x, modulus):
    if x == 0:
        return 0

    # ensure x is a residue mod the modulus
    if not 0 < x < modulus:
        return compute_jacobi_symbol(
            x % modulus, modulus
        )

    # trivial case
    if x == 1:
        return 1

    # base case given by quadratic reciprocity
    if x == 2:
        if modulus % 8 == 1 or modulus % 8 == 7:
            return 1
        return -1

    # divide out the largest even factor
    even_factorization = EvenFactorization.factor(x)
    if even_factorization.two_power > 0:
        return (
            pow(compute_jacobi_symbol(2, modulus), even_factorization.two_power)
            * compute_jacobi_symbol(even_factorization.base, modulus)
        )

    # another base case given by quadratic reciprocity
    if x == modulus - 1:
        if modulus % 4 == 1:
            return 1
        return -1

    # recursive case given by quadratic reciprocity
    if x % 4 == 1 or modulus % 4 == 1:
        return compute_jacobi_symbol(modulus, x)

    return -1 * compute_jacobi_symbol(modulus, x)