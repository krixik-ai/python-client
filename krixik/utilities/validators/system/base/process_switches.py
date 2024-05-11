def process_switches_checker(*, process_for_vector_search: bool, process_for_keyword_search: bool) -> None:
    if process_for_vector_search is not None and process_for_keyword_search is not None:
        # check processing switches
        if not isinstance(process_for_vector_search, bool):
            raise TypeError("process_for_vector_search must be a bool")

        if not isinstance(process_for_keyword_search, bool):
            raise TypeError("process_for_keyword_search must be a bool")

        if process_for_vector_search is False and process_for_keyword_search is False:
            raise ValueError("process_for_vector_search and process_for_keyword_search cannot both be False")
