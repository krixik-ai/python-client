def sort_order_checker(sort_order: str) -> None:
    if sort_order is not None:
        # check that sort_order is a string
        if not isinstance(sort_order, str):
            raise TypeError(f"sort_order: must be a string - the sort_order entered is not in this required form - {sort_order}")

        if sort_order not in ["ascending", "descending", "global"]:
            raise ValueError(
                f"sort_order: must be one of the following strings: 'ascending', 'descending', or 'global (if using vector_search only)'.  The sort_order entered is not in this required form - {sort_order}"
            )
