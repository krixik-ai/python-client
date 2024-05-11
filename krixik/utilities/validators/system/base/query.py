from krixik.utilities.validators import Q_MIN, Q_MAX
from krixik.utilities.utilities import invalid_char_check


def query_checker(query: str) -> None:
    if query is not None:
        # check that query is a string
        if not isinstance(query, str):
            raise TypeError(f"invalid query: not a string - {query}")

        # strip query of whitespace
        query = query.strip()

        # check that query length is greater than Q_MIN
        if len(query) <= Q_MIN:
            raise ValueError(f"invalid query: length is less than {Q_MIN} characters (current minimum length allowable): {query}")

        # check that query length is less than Q_MAX
        if len(query) > Q_MAX:
            raise ValueError(f"invalid query: length is greater than {Q_MAX} characters (current maximum length allowable) - {query}")

        # # check that query contains only acceptable characters
        # invalid_char = invalid_char_check(query)

        # if len(invalid_char) > 0:
        #     raise ValueError(
        #         f"invalid query: please remove or replace the following invalid characters - {invalid_char}"
        #     )
