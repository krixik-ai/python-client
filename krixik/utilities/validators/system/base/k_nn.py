from krixik.utilities.validators import K_MIN
from krixik.utilities.validators import K_MAX


def k_checker(k: int | None = None) -> None:
    if k is not None:
        # check that k is an int, greater than 0, and less than or equal to 10
        if not isinstance(k, int) or isinstance(k, bool):
            raise TypeError(f"k must be an int greater than {K_MIN} and less than or equal to {K_MAX}")

        if k < K_MIN:
            raise ValueError(f"k must be an int greater than {K_MIN} and less than or equal to {K_MAX}")

        if k > K_MAX:
            raise ValueError(f"k must be an int greater than {K_MIN} and less than or equal to {K_MAX}")
