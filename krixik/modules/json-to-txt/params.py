CHUNK_SIZE_MIN = 3
CHUNK_SIZE_MAX = 20
OVERLAP_SIZE_MIN = 1


def fixed_params_validator(params: dict) -> None:
    params_key_options = ["chunk_size", "overlap_size"]
    if params is not None:
        if not isinstance(params, dict):
            raise TypeError(
                f"params: must be a dictionary with unique key(s): chunk_size, overlap_size - the params entered is not in this required form - {params}"
            )

        # if params is length 0, then return 1
        if len(params) == 0:
            raise ValueError(
                f"params: must be a dictionary with unique key(s): chunk_size, overlap_size - the params entered is not in this required form - {params}"
            )

        # check that only two keys are in params
        if len(params.keys()) > 2:
            raise ValueError(
                f"params: must be a dictionary with unique key(s): chunk_size, overlap_size - the params entered is not in this required form - {params}"
            )

        # check that params has all required keys
        for key in params.keys():
            if key not in params_key_options:
                raise ValueError(
                    f"params: must be a dictionary with unique key(s): chunk_size, overlap_size - the params entered is not in this required form - {params}"
                )

        # check that params values are all ints
        for value in params.values():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"params: all values must be integers - the params entered is not in this required form - {params}")

        # check that no key is repeated
        if len(params.keys()) != len(set(params.keys())):
            raise ValueError(
                f"params: must be a dictionary with unique key(s): chunk_size, overlap_size - the params entered is not in this required form - {params}"
            )

        # check that chunk_size is an integer
        if "chunk_size" in params.keys():
            if not isinstance(params["chunk_size"], int) or isinstance(params["chunk_size"], bool):
                raise TypeError(f"params: chunk_size must be an integer - the params entered is not in this required form - {params}")

            # check that chunk_size is greater than CHUNK_SIZE_MIN
            if params["chunk_size"] <= CHUNK_SIZE_MIN:
                raise ValueError(
                    f"params: chunk_size must be greater than {CHUNK_SIZE_MIN} - the params entered is not in this required form - {params}"
                )

            # check that chunk_size is no greater than CHUNK_SIZE_MAX
            if params["chunk_size"] > CHUNK_SIZE_MAX:
                raise ValueError(
                    f"params: chunk_size must be no greater than {CHUNK_SIZE_MAX} - the params entered is not in this required form - {params}"
                )

        else:
            raise ValueError(f"params: chunk_size must be in params - the params entered is not in this required form - {params}")

        # check that overlap_size is an integer
        if "overlap_size" in params.keys():
            if not isinstance(params["overlap_size"], int) or isinstance(params["overlap_size"], bool):
                raise TypeError(f"params: overlap_size must be an integer - the params entered is not in this required form - {params}")

            # check that overlap_size is greater than or equal to OVERLAP_SIZE_MIN
            if params["overlap_size"] < OVERLAP_SIZE_MIN:
                raise ValueError(
                    f"params: overlap_size must be greater than or equal to {OVERLAP_SIZE_MIN} - the params entered is not in this required form - {params}"
                )

            # check that overlap_size is no greater than chunk_size - 1
            if params["overlap_size"] > params["chunk_size"] - 1:
                raise ValueError(
                    f"params: overlap_size must be no greater than chunk_size - 1 - the params entered is not in this required form - {params}"
                )
        else:
            raise ValueError(f"params: overlap_size must be in params - the params entered is not in this required form - {params}")

        # check that if chunk_size or overlap_size is in params, then both are in params
        if "chunk_size" in params.keys() and "overlap_size" not in params.keys():
            raise ValueError(
                f"params: if chunk_size is in params, then overlap_size must also be in params - the params entered is not in this required form - {params}"
            )

        if "overlap_size" in params.keys() and "chunk_size" not in params.keys():
            raise ValueError(
                f"params: if overlap_size is in params, then chunk_size must also be in params - the params entered is not in this required form - {params}"
            )
