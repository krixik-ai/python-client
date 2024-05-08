def quantize_validator(params: dict) -> None:
    if "quantize" not in list(params.keys()):
        raise ValueError(f"params: must have a key named 'quantize' - the params entered are not in this required form - {params}")
    if not isinstance(params["quantize"], bool):
        raise TypeError(f"quantize: must be a boolean - the quantize entered is not in this required form - {quantize}")
